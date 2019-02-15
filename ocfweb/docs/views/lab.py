from datetime import date
from datetime import timedelta

from django.shortcuts import render
from ocflib.lab.hours import Day
from ocflib.lab.hours import HOLIDAYS

from ocfweb.api.hours import display_hours


def lab(doc, request):
    return render(
        request,
        'docs/lab.html',
        {
            'title': doc.title,
            'description': (
                'The Open Computing Facility computer lab is a '
                'free and open-source computer lab located on the '
                'UC Berkeley campus, maintained by OCF volunteers.'
            ),
            'hours_this_week': [
                Day.from_date(date.today() + timedelta(days=i))
                for i in range(7)
            ],
            'regular_hours': display_hours(),
            # Format dates to look like "month day, year" but with non-breaking
            # spaces (\xa0) instead of spaces so that the date does not get
            # broken up across lines:
            # https://docs.djangoproject.com/en/2.0/ref/templates/builtins/#date
            'holiday_format': 'M\xa0j,\xa0o',
            # Only select current and future holidays (any that have not finished fully)
            'holidays': [holiday for holiday in HOLIDAYS if holiday[1] >= date.today()],
            'SUNDAY': Day.SUNDAY,
            'MONDAY': Day.MONDAY,
            'TUESDAY': Day.TUESDAY,
            'WEDNESDAY': Day.WEDNESDAY,
            'THURSDAY': Day.THURSDAY,
            'FRIDAY': Day.FRIDAY,
            'SATURDAY': Day.SATURDAY,
        },
    )
