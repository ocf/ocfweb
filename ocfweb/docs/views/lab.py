from datetime import date
from datetime import timedelta

from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render

from ocfweb.api.hours import get_hours_listing
from ocfweb.docs.doc import Document


def lab(doc: Document, request: HttpRequest) -> HttpResponse:
    hours_listing = get_hours_listing()
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
                (
                    date.today() + timedelta(days=i),
                    hours_listing.hours_on_date(date.today() + timedelta(days=i)),
                )
                for i in range(7)
            ],
            'regular_hours': hours_listing.regular,
            # Format dates to look like "month day, year" but with non-breaking
            # spaces (\xa0) instead of spaces so that the date does not get
            # broken up across lines:
            # https://docs.djangoproject.com/en/2.0/ref/templates/builtins/#date
            'holiday_format': 'M\xa0j,\xa0o',
            # Only select current and future holidays (any that have not finished fully)
            'holidays': [
                holiday
                for holiday in hours_listing.holidays
                if holiday.enddate >= date.today()
            ],
        },
    )
