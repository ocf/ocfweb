from datetime import datetime

from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render
from ocflib.printing.quota import get_connection
from ocflib.printing.quota import get_quota

from ocfweb.auth import login_required
from ocfweb.component.session import logged_in_user
# from datetime import timedelta


def _relative_timestr(timestamp: datetime) -> str:
    """
    Compare timestamp to now and return a relative time string (e.g. "in 2 hours")
    """
    now = datetime.now()

    diff = (timestamp - now).total_seconds() / 3600

    if diff < 0:
        return 'expired'
    elif diff < 1:
        return 'in <1 hour'
    elif diff < 2:
        return 'in 1 hour'
    else:
        return f'in {int(diff)} hours'


@login_required
def webprint_home(request: HttpRequest) -> HttpResponse:
    """
    Webprinting home page.
    """
    with get_connection() as c:
        quota = get_quota(c, logged_in_user(request))

        return render(
            request,
            'webprint/home.html',
            {
                'title': 'Web Printing',
                'remaining_pages_day': quota.daily,
                'remaining_pages_semester': quota.semesterly,
                'pending_requests': [
                    # {
                    #     "id": 3,
                    #     "document": "Jane Doe.pdf",
                    #     "pages": 2,
                    #     "expiry": _relative_timestr(
                    #         datetime.now() + timedelta(minutes=30)
                    #     ),
                    #     "printed": False,
                    # },
                    # {
                    #     "id": 1,
                    #     "document": "Bob John.pdf",
                    #     "pages": 10,
                    #     "expiry": _relative_timestr(
                    #         datetime.now() + timedelta(hours=1, minutes=20)
                    #     ),
                    #     "printed": False,
                    # },
                    # {
                    #     "id": 2,
                    #     "document": "John Doe.pdf",
                    #     "pages": 8,
                    #     "expiry": _relative_timestr(
                    #         datetime.now() + timedelta(hours=7, minutes=40)
                    #     ),
                    #     "printed": True,
                    # },
                ],
            },
        )
