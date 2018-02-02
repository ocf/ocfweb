from collections import namedtuple
from datetime import date
from datetime import datetime
from datetime import time

from cached_property import cached_property
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from ocfweb.component.blog import get_blog_posts

announcements = ()


class Announcement(namedtuple('Announcement', ('title', 'date', 'path', 'render'))):

    @cached_property
    def link(self):
        return reverse(self.route_name)

    @cached_property
    def route_name(self):
        return '{}-announcement'.format(self.path)

    @cached_property
    def datetime(self):
        """This is pretty silly, but Django humanize needs a datetime."""
        return timezone.make_aware(
            datetime.combine(self.date, time()),
            timezone.get_default_timezone(),
        )


def announcement(title, date, path):
    def wrapper(fn):
        global announcements
        announcements += (
            Announcement(
                title=title,
                date=date,
                path=path,
                render=lambda request: fn(title, request),
            ),
        )
        return fn
    return wrapper


def index(request):
    return render(
        request,
        'announcements/index.html',
        {
            'title': 'News from the staff team',

            'announcements': sorted(
                announcements,
                key=lambda announcement: announcement.date,
                reverse=True,
            ),
            'blog_posts': get_blog_posts()[:10],
        },
    )


@announcement(
    "OCF affirms support for EFF's Electronic Frontier Alliance",
    date(2016, 5, 12),
    'ocf-eff-alliance',
)
def eff_alliance(title, request):
    return render(
        request,
        'announcements/2016-05-12-ocf-eff-alliance.html',
        {
            'title': title,
        },
    )


@announcement(
    'Unveiling a new name for the Open Computing Facility',
    date(2016, 4, 1),
    'renaming-ocf',
)
def renaming_announcement(title, request):
    return render(
        request,
        'announcements/2016-04-01-renaming.html',
        {
            'title': title,
            'og_title': title,
            'og_image': request.build_absolute_uri(static('img/announcements/thanks-for-flying-ofc-og.png')),
            'description': (
                'The Board of Directors has voted to rename the Open Computing Facility '
                'to the Open Facility for Computing (OFC).'
            ),
        },
    )


@announcement(
    'Changes to printing policies',
    date(2016, 2, 9),
    'printing',
)
def printing_announcement(title, request):
    return render(
        request,
        'announcements/2016-02-09-printing.html',
        {
            'title': title,
        },
    )


@announcement(
    'OCF seeking interest in high-performance computing service',
    date(2017, 3, 1),
    'hpc-survey',
)
def hpc_survey(title, request):
    return render(
        request,
        'announcements/2017-03-01-hpc-survey.html',
        {
            'title': title,
        },
    )


@announcement(
    'The OCF is hiring!',
    date(2017, 3, 20),
    'hiring',
)
def hiring(title, request):
    return render(
        request,
        'announcements/2017-03-20-hiring.html',
        {
            'title': title,
        },
    )
