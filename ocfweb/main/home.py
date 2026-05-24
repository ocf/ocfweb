import random
from datetime import date
from datetime import timedelta
from operator import attrgetter
from typing import Mapping

from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from ocflib.lab.staff_hours import get_staff_hours_soonest_first
from ocflib.vhost.web import get_vhosts

from ocfweb.api.hours import get_hours_listing
from ocfweb.caching import periodic
from ocfweb.component.blog import get_blog_posts
from ocfweb.component.blog import get_news_posts
from ocfweb.component.lab_status import get_lab_status


@periodic(60)
def get_staff_hours() -> str:
    return get_staff_hours_soonest_first()[:2]


def hosted_site_urls(vhosts: Mapping[str, object] | None = None) -> list[str]:
    if vhosts is None:
        vhosts = get_vhosts()

    return sorted(
        f'https://{hostname}/'
        for hostname in vhosts.keys()
    )


def random_hosted_site(request: HttpRequest) -> HttpResponseRedirect:
    return redirect(random.choice(hosted_site_urls()))


def home(request: HttpRequest) -> HttpResponse:
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
                get_blog_posts() + get_news_posts(), key=attrgetter('datetime'),
                reverse=True,
            )[:3],
            'today': hours[0],
            'lab_status': get_lab_status(),
        },
    )
