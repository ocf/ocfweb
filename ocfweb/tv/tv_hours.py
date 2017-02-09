from django.shortcuts import render
from ocflib.lab.hours import Day


def tv_hours(request):
    return render(
        request,
        'tv/hours.html',
        {
            'hours': Day.from_date(),
        },
    )
