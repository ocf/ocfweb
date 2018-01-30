import time
from datetime import date
from datetime import timedelta

from django.shortcuts import render
from ocflib.lab.hours import Day
from ocflib.lab.staff_hours import get_staff_hours as real_get_staff_hours

from ocfweb.caching import periodic
from ocfweb.component.lab_status import get_lab_status


@periodic(60, ttl=86400)
def get_staff_hours():
    return real_get_staff_hours()


def rotate_list(lst, shift):
    return lst[shift:] + lst[:shift]


def sort_days_of_week(Days):
    for index in range(len(Days)):
        if Days[index].weekday == 'Monday':
            return rotate_list(Days, index)


def weekend(day):
    return day.weekday == 'Sunday' or day.weekday == 'Saturday'


def remove_weekends(Days):
    index = 0
    while index < len(Days):
        if weekend(Days[index]):
            Days.pop(index)
        else:
            index += 1
    return Days


def staff_hours(request):
    print(get_staff_hours())
    return render(
        request,
        'main/staff-hours.html',
        {
            'title': 'Staff Hours',
            'staff_hours': get_staff_hours(),
            'today': time.strftime('%A'),
            'lab_status': get_lab_status(),
            'days_of_the_week': sort_days_of_week(remove_weekends([
                Day.from_date(date.today() + timedelta(days=i))
                for i in range(7)
            ])),
        },
    )
