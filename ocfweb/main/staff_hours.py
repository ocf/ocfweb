import time

from django.shortcuts import render
from ocflib.lab.staff_hours import get_staff_hours as real_get_staff_hours

from ocfweb.caching import periodic
from ocfweb.component.lab_status import get_lab_status


@periodic(60, ttl=86400)
def get_staff_hours():
    return real_get_staff_hours()


def staff_hours(request):
    return render(
        request,
        'main/staff-hours.html',
        {
            'title': 'Staff Hours',
            'staff_hours': get_staff_hours(),
            'today': time.strftime('%A'),
            'lab_status': get_lab_status(),
            'days_of_the_week':['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',\
                    'Saturday', 'Sunday'],
        },
    )
