from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render
from ocflib.printing.quota import get_connection
from ocflib.printing.quota import get_quota

from ocfweb.auth import login_required
from ocfweb.component.session import logged_in_user


@login_required
def new_print_request(request: HttpRequest) -> HttpResponse:
    with get_connection() as c:
        quota = get_quota(c, logged_in_user(request))

        return render(
            request,
            'webprint/new.html',
            {
                'title': 'New Print Request',
                'remaining_pages_day': quota.daily,
                'remaining_pages_semester': quota.semesterly,
            },
        )
