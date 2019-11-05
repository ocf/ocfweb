from collections import namedtuple
from datetime import date
from datetime import datetime as original_datetime
from datetime import time
from typing import Any
from typing import Callable
from typing import Tuple

from cached_property import cached_property
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.templatetags.static import static
from django.urls import reverse
from django.utils import timezone

from ocfweb.component.blog import get_blog_posts

announcements: Tuple['Announcement', ...] = ()


class Announcement(namedtuple('Announcement', ('title', 'date', 'path', 'render'))):

    @cached_property
    def link(self) -> str:
        return reverse(self.route_name)

    @cached_property
    def route_name(self) -> str:
        return f'{self.path}-announcement'

    @cached_property
    def datetime(self) -> original_datetime:
        """This is pretty silly, but Django humanize needs a datetime."""
        return timezone.make_aware(
            original_datetime.combine(self.date, time()),
            timezone.get_default_timezone(),
        )


def announcement(title: str, date: date, path: str) -> Callable[[Any], Any]:
    def wrapper(fn: Callable[..., Any]) -> Callable[..., Any]:
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


def index(request: HttpRequest) -> HttpResponse:
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
def eff_alliance(title: str, request: HttpRequest) -> HttpResponse:
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
def renaming_announcement(title: str, request: HttpRequest) -> HttpResponse:
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
def printing_announcement(title: str, request: HttpRequest) -> HttpResponse:
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
def hpc_survey(title: str, request: HttpRequest) -> HttpResponse:
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
    'hiring-2017',
)
def hiring_2017(title: str, request: HttpRequest) -> HttpResponse:
    return render(
        request,
        'announcements/2017-03-20-hiring.html',
        {
            'title': title,
        },
    )


@announcement(
    'The OCF is hiring!',
    date(2018, 10, 30),
    'hiring-2018',
)
def hiring_2018(title: str, request: HttpRequest) -> HttpResponse:
    return render(
        request,
        'announcements/2018-10-30-hiring.html',
        {
            'title': title,
        },
    )
