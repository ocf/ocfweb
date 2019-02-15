from django.shortcuts import redirect
from django.shortcuts import render

from ocfweb.api.hours import get_hours_listing


def tv_main(request):
    return render(
        request,
        'tv/tv.html',
        {
            'hours': get_hours_listing().hours_on_date(),
        },
    )


def tv_labmap(request):
    return redirect('https://labmap.ocf.berkeley.edu/')
