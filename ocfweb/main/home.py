from datetime import date
from datetime import timedelta
from operator import attrgetter
from typing import Any

from django.http import HttpResponse
from django.shortcuts import render
from ocflib.lab.staff_hours import get_staff_hours_soonest_first

from ocfweb.announcements.announcements import announcements
from ocfweb.api.hours import get_hours_listing
from ocfweb.caching import periodic
from ocfweb.component.blog import get_blog_posts
from ocfweb.component.lab_status import get_lab_status


@periodic(60, ttl=86400)
def get_staff_hours() -> str:
    return get_staff_hours_soonest_first()[:2]


def home(request: Any) -> HttpResponse:
    hours_listing = get_hours_listing()
    hours = [
        (
            date.today() + timedelta(days=i),
            hours_listing.hours_on_date(date.today() + timedelta(days=i)),
        )
        for i in range(3)
    ]
    return render(
        request,
        'main/home.html',
        {
            'fulltitle': 'Open Computing Facility at UC Berkeley',
            'description': (
                'The Open Computing Facility is an all-volunteer student '
                'organization dedicated to free and open-source computing for all UC '
                'Berkeley students.'
            ),
            'staff_hours': get_staff_hours(),
            'hours': hours,
            'announcements': sorted(
                get_blog_posts() + list(announcements), key=attrgetter('datetime'),
                reverse=True,
            )[:2],
            'today': hours[0],
            'lab_status': get_lab_status(),
        },
    )
