import operator
from collections import namedtuple
from datetime import date
from datetime import datetime
from datetime import timedelta

import requests
from django.http import JsonResponse

from ocfweb.caching import periodic

HOURS_SPREADSHEET = 'https://docs.google.com/spreadsheet/ccc?key=1FHgW0wCnAh49bZIw54eoBT9xEoJ3AGG7Y2LhQdi0Lvs&output=csv'  # noqa: E501
SHIFT_LENGTH = timedelta(hours=1)


class Hour(namedtuple('Hours', ['open', 'close', 'staffer'])):

    def __contains__(self, when):
        if isinstance(when, datetime):
            when = when.time()

        return self.open <= when < self.close


def _get_hours():
    """pull hours from the Google spreadsheet and parse shifts."""

    response = requests.get(HOURS_SPREADSHEET)
    response.raise_for_status()

    matrix = response.text.splitlines()
    matrix = [row.split(',') for row in matrix]

    # row[0] = ['13:30PM', 'name1', 'name2', ...]
    shifts = [row[0] for row in matrix]

    # first row is a header, first col is times: ['', 'Monday', ...]
    header = shifts.pop(0)
    assert header == '', header

    all_shifts = {}

    # instead of e.g. enumerate(['Monday', 'Tuesday', ... 'Sunday'])
    for day in range(7):
        # matrix[sidx + 1][day + 1] = person on shift on that shift index
        all_shifts[day] = {
            shift: matrix[sidx + 1][day + 1] for sidx, shift in enumerate(shifts)
        }

    #  this will get cached downstream
    return all_shifts


def _merge_shifts(first, second, staffer=True):
    return Hour(
        open=min(first.open, second.open),
        close=max(first.close, second.close),
        staffer=first.staffer if staffer else None,
    )


def _combine_shifts(shifts):
    """combine a list of shifts into a list of Hour()s.

    >>> _combine_shifts({'16:00PM':'test1', '16:30PM':'test2', ...})
    [Hour(open=time(16), close=time(17), staffer='test2'), ...]
    """

    raw_shifts = []
    for shift, staffer in shifts.items():
        if not staffer:  # skip unstaffed shifts
            continue

        open = datetime.strptime(shift, '%I:%M %p')  # 12-hour AM/PM i.e. 7:00PM
        close = open + SHIFT_LENGTH
        raw_shifts.append(Hour(open=open.time(), close=close.time(), staffer=staffer))

    raw_shifts.sort(key=operator.attrgetter('open'))

    combined_shifts = []

    shift = raw_shifts.pop(0)
    for next_shift in raw_shifts:
        if (shift.close in next_shift or next_shift.close in shift) and \
                shift.staffer == next_shift.staffer:
            shift = _merge_shifts(shift, next_shift)
        else:
            combined_shifts.append(shift)
            shift = next_shift

    # tail case where staffer condition doesn't trip on list end
    combined_shifts.append(shift)

    return combined_shifts


def _generate_regular_hours():
    raw_hours = _get_hours()
    return {day: _combine_shifts(shifts) for day, shifts in raw_hours.items()}


@periodic(5 * 60)
def display_hours():
    """merge shifts even further for display.

    ocflib previously provided a list of hours separated when there
    were discontinuous shifts. This hours implementation separates
    hours when different opstaff are on shift as well for future big
    brother tracking purposes, but this breaks applications that depend on
    a concise list of hours for display. This is a fix that presents hours
    like the old implementation until the code can be refactored as part
    of the overall big brother project, i.e., in ocflib.
    """

    regular_hours = _generate_regular_hours()

    display_hours = {}

    for day, hours in regular_hours.items():
        merged_shifts = []

        hour = hours.pop(0)
        for next_hour in hours:
            if hour.close in next_hour or next_hour.close in hour:
                hour = _merge_shifts(hour, next_hour, False)
            else:
                merged_shifts.append(hour)
                hour = next_hour

        merged_shifts.append(hour)

        display_hours[day] = merged_shifts

    return display_hours


def get_hours_all(request):
    return JsonResponse(
        display_hours(),
        json_dumps_params={'default': lambda x: x.isoformat()},
    )


def get_hours_today(request):
    return JsonResponse(
        display_hours()[date.today().weekday()],
        json_dumps_params={'default': lambda x: x.isoformat()},
        safe=False,
    )
