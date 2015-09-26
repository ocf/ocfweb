from datetime import date
from datetime import timedelta

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import timezone
from ocflib.lab.hours import get_hours
from ocflib.lab.staff_hours import get_staff_hours_soonest_first

from ocfweb.component.banner import get_banner_message
from ocfweb.component.blog import get_blog_posts


def home(request):
    hours = [
        get_hours(date.today() + timedelta(days=i)) for i in range(7)
    ]

    blog_posts = [
        post for post
        in get_blog_posts()
        if timezone.now() - post.published < timedelta(days=365)
    ][:2]

    banner = get_banner_message()

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
            'hours': hours,
            'today': hours[0],
            'blog_posts': blog_posts,
            'banner': banner,
        },
        context_instance=RequestContext(request),
    )
