from typing import Any

from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render

from ocfweb.api.hours import get_hours_listing


def tv_main(request: Any) -> HttpResponse:
    return render(
        request,
        'tv/tv.html',
        {
            'hours': get_hours_listing().hours_on_date(),
        },
    )


def tv_labmap(request: Any) -> HttpResponse:
    return redirect('https://labmap.ocf.berkeley.edu/')
