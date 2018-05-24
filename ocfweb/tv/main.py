from django.shortcuts import render
from ocflib.lab.hours import Day


def tv_main(request):
    return render(
        request,
        'tv/tv.html',
        {
            'hours': Day.from_date(),
        },
    )


def tv_labmap(request):
    return render(
        request,
        'tv/labmap.html',
        {
            'hours': [[h.open.hour, h.close.hour] for h in Day.from_date().hours],
        },
    )
