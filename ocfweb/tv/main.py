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
