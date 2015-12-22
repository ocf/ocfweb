from datetime import date
from datetime import timedelta

from django.shortcuts import render
from ocflib.lab.hours import Day
from ocflib.lab.staff_hours import get_staff_hours_soonest_first

from ocfweb.caching import periodic
from ocfweb.component.blog import get_blog_posts
from ocfweb.component.lab_status import get_lab_status


@periodic(60)
def get_staff_hours():
    return get_staff_hours_soonest_first()[:2]


def home(request):
    hours = [Day.from_date(date.today() + timedelta(days=i)) for i in range(3)]
    return render(
        request,
        'home.html',
        {
            'fulltitle': 'Open Computing Facility at UC Berkeley',
            'description': (
                'The Open Computing Facility is an all-volunteer student '
                'organization dedicated to free and open-source computing for all UC '
                'Berkeley students.'
            ),
            'staff_hours': get_staff_hours(),
            'hours': hours,
            'today': hours[0],
            'blog_posts': get_blog_posts()[:2],
            'lab_status': get_lab_status(),
        },
    )
