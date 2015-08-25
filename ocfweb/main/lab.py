from datetime import date
from datetime import timedelta

from django.shortcuts import render_to_response
from django.template import RequestContext
from ocflib.lab.hours import get_hours


def lab(request):
    today = date.today()
    hours_next_week = [
        get_hours(today + timedelta(days=i)) for i in range(4)
    ]

    return render_to_response(
        'lab.html',
        {
            'title': 'Computer Lab – Free & Open Source',
            'hours_next_week': hours_next_week,
        },
        context_instance=RequestContext(request),
    )
