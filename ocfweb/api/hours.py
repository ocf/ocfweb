from collections import namedtuple
from datetime import date
from datetime import datetime
from datetime import time
from datetime import timedelta

import requests
from django.http import JsonResponse

from ocfweb.caching import periodic

HOURS_SPREADSHEET = 'https://docs.google.com/spreadsheet/ccc?key=1WgczUrxqey63fmPRmdkCDMCbsfaTyCJrixiCeJj35UI&output=csv'  # noqa: E501
SHIFT_LENGTH = timedelta(hours=0.5)


class Hour(namedtuple('Hours', ['open', 'close', 'staffer'])):

    def __contains__(self, when):
        if not isinstance(when, time):
            when = when.time()

        return self.open <= when < self.close


def _get_hours():
    """pull hours from the Google spreadsheet"""

    response = requests.get(HOURS_SPREADSHEET)
    response.raise_for_status()

    matrix = response.content.decode('utf-8').splitlines()
    matrix = [row.split(',') for row in matrix]

    # [1:] because the first box in the matrix is empty
    # matrix[0] = ['', 'Monday', 'Tuesday', ...]
    # row[0] = ['13:30PM', 'name1', 'name2', ...]
    shifts = [row[0] for row in matrix][1:]

    all_shifts = {}

    # instead of e.g. enumerate(['Monday', 'Tuesday', ... 'Sunday'])
    for day in range(7):
        # matrix[sidx + 1][day + 1] = person on shift on that shift index
        all_shifts[day] = {shift: matrix[sidx + 1][day + 1] for sidx, shift in enumerate(shifts)}

    #  this will get cached downstream
    return all_shifts


def _combine_shifts(shifts):
    """combined a day's worht of shifts into a list of Hour() objects
       shifts = {'09:00AM': 'name1', ...}"""

    raw_shifts = []
    for shift, staffer in shifts.items():
        if not staffer:  # skip unstaffed shifts
            continue

        open = datetime.strptime(shift, '%H:%M%p')  # 16:00PM
        close = open + SHIFT_LENGTH
        raw_shifts.append(Hour(open=open.time(), close=close.time(), staffer=staffer))

    raw_shifts.sort(key=lambda k: k.open)

    combined_shifts = []

    initial = raw_shifts[0]
    for next_shift in raw_shifts[1:]:
        if (initial.close in next_shift or next_shift.close in initial) and \
                initial.staffer == next_shift.staffer:
            initial = Hour(
                open=min(initial.open, next_shift.open),
                close=max(initial.close, next_shift.close),
                staffer=initial.staffer,
            )
        else:
            combined_shifts.append(initial)
            initial = next_shift

    combined_shifts.append(initial)  # tail case where staffer condition doesn't trip on list end
    return combined_shifts


@periodic(5 * 60)
def _generate_regular_hours():
    raw_hours = _get_hours()
    return {day: _combine_shifts(shifts) for day, shifts in raw_hours.items()}


def get_hours_all(request):
    return JsonResponse(
        _generate_regular_hours(),
        json_dumps_params={'default': lambda x: x.isoformat()},
        content_type='application/json',
    )


def get_hours_today(request):
    return JsonResponse(
        _generate_regular_hours()[date.today().weekday()],
        json_dumps_params={'default': lambda x: x.isoformat()},
        content_type='application/json',
        safe=False,
    )
