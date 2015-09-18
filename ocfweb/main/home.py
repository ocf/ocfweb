from datetime import date
from datetime import timedelta

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import timezone
from ocflib.lab.hours import get_hours
from ocflib.lab.staff_hours import get_staff_hours_soonest_first

from ocfweb.component.blog import get_blog_posts


def home(request):
    today = date.today()
    sidebar_hours = [
        get_hours(today + timedelta(days=i)) for i in range(4)
    ]

    blog_posts = [
        post for post
        in get_blog_posts()
        if timezone.now() - post.published < timedelta(days=365)
    ][:2]

    return render_to_response(
        'home.html',
        {
            'fulltitle': 'Open Computing Facility at UC Berkeley',
            'description': (
                'The Open Computing Facility is an all-volunteer student '
                'organization dedicated to free and open-source computing for all UC '
                'Berkeley students.'''
            ),
            'staff_hours': get_staff_hours_soonest_first()[:2],
            'hours_columns': [sidebar_hours[:2], sidebar_hours[2:]],
            'blog_posts': blog_posts,
        },
        context_instance=RequestContext(request),
    )
