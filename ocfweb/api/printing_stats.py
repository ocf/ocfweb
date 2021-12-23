from datetime import date
from datetime import timedelta

from django.http import HttpRequest
from django.http import JsonResponse

from ocfweb.stats.printing import _pages_per_day
from ocfweb.stats.printing import _pages_printed_data
from ocfweb.stats.printing import _toner_changes
from ocfweb.stats.printing import ACTIVE_PRINTERS

# Stats that show up on stats/printing page


def get_pages_per_day(request: HttpRequest) -> JsonResponse:
    pages_per_day = _pages_per_day()

    # Pages in last 30 days, with date strings instead of datetime objects
    pages_last_30 = {}

    rn = date.today()
    last_month = [rn - timedelta(days=x) for x in range(30)]
    for day in last_month:
        day_str = day.strftime('%a %b %d, %Y')
        pages_last_30[day_str] = {'total': sum(pages_per_day[day].values())}
        for printer in ACTIVE_PRINTERS:
            pages_last_30[day_str][printer] = pages_per_day[day][printer]

    response = JsonResponse(
        pages_last_30,
        safe=False,
    )
    response['Access-Control-Allow-Origin'] = '*'
    return response


def get_active_printers(request: HttpRequest) -> JsonResponse:
    response = JsonResponse(
        ACTIVE_PRINTERS,
        safe=False,
    )
    response['Access-Control-Allow-Origin'] = '*'
    return response


def get_lifetime_data(request: HttpRequest) -> JsonResponse:
    response = JsonResponse(
        _pages_printed_data(),
        safe=False,
    )
    response['Access-Control-Allow-Origin'] = '*'
    return response


def get_toner_changes(request: HttpRequest) -> JsonResponse:
    response = JsonResponse(
        _toner_changes(),
        safe=False,
    )
    response['Access-Control-Allow-Origin'] = '*'
    return response
