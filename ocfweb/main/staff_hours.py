import time

from django.shortcuts import render
from ocflib.lab.staff_hours import get_staff_hours as real_get_staff_hours
from datetime import date
from datetime import timedelta

from ocflib.lab.hours import Day

from ocfweb.caching import periodic
from ocfweb.component.lab_status import get_lab_status


@periodic(60, ttl=86400)
def get_staff_hours():
    return real_get_staff_hours()

"""
Assumes that staff hours are only on weekdays. If days of staff hours change,
add or take out of weekdays list.
"""
def staff_hours(request):
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    return render(
        request,
        'main/staff-hours.html',
        {
            'title': 'Staff Hours',
            'staff_hours': get_staff_hours(),
            'today': time.strftime('%A'),
            'lab_status': get_lab_status(),
            'days_of_the_week': weekdays,
            'hours_this_week': [
                Day.from_date(date.today() + timedelta(days=i))
                for i in range(7)
            ],
        },
    )
