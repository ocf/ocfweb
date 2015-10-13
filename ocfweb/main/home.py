from datetime import date
from datetime import timedelta

from django.shortcuts import render_to_response
from django.template import RequestContext
from ocflib.lab.hours import Day
from ocflib.lab.staff_hours import get_staff_hours_soonest_first
from requests.exceptions import RequestException

from ocfweb.caching import ttl_cache
from ocfweb.component.blog import get_blog_posts
from ocfweb.component.lab_status import get_lab_status


@ttl_cache(ttl=60)
def get_staff_hours():
    return get_staff_hours_soonest_first()[:2]


def home(request):
    try:
        # fetching blog posts is hella flaky, we don't want to 500 if it fails
        # TODO: do in a background job to avoid this
        blog_posts = get_blog_posts()[:2]
    except RequestException:
        blog_posts = []

    hours = [Day.from_date(date.today() + timedelta(days=i)) for i in range(3)]
    return render_to_response(
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
            'blog_posts': blog_posts,
            'lab_status': get_lab_status(),
        },
        context_instance=RequestContext(request),
    )
