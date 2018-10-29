from datetime import date
from datetime import timedelta
from operator import attrgetter

from django.shortcuts import render
from ocflib.lab.hours import Day
from ocflib.lab.staff_hours import get_staff_hours_soonest_first

from ocfweb.announcements.announcements import announcements
from ocfweb.caching import periodic
from ocfweb.component.blog import get_blog_posts
from ocfweb.component.lab_status import get_lab_status


from ocflib.lab.hours import HOLIDAYS
from ocfweb.api.hours import display_hours


@periodic(60, ttl=86400)
def get_staff_hours():
    return get_staff_hours_soonest_first()[:2]


def home(request):
    hours = [Day.from_date(date.today() + timedelta(days=i)) for i in range(7)]
    return render(
        request,
        'main/home.html',
        {
            'fulltitle': 'Open Computing Facility at UC Berkeley',
            'description': (
                'The Open Computing Facility is an all-volunteer student '
                'organization dedicated to free and open-source computing for all UC '
                'Berkeley students.'
            ),
            'staff_hours': get_staff_hours(),
            'regular_hours': display_hours(),
            'hours': hours,
            'announcements': sorted(
                get_blog_posts() + list(announcements), key=attrgetter('datetime'),
                reverse=True,
            )[:2],
            'today': hours[0],
            'lab_status': get_lab_status(),

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
