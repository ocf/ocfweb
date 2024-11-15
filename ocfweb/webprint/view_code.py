from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render

from ocfweb.auth import login_required
# from ocflib.printing.quota import get_connection
# from ocflib.printing.quota import get_quota
# from ocfweb.component.session import logged_in_user


@login_required
def view_webprint_code(request: HttpRequest) -> HttpResponse:
    # request_id = request.GET.get('request_id')
    return render(
        request,
        'webprint/view_code.html',
        {
            'title': 'View Print Code',
        },
    )
