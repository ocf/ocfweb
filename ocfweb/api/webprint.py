from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.views.decorators.http import require_POST

from ocfweb.auth import login_required
# from ocfweb.component.session import logged_in_user
# from ocflib.printing.quota import get_connection
# from ocflib.printing.quota import get_quota


@require_POST
@login_required
def submit_print_request(request: HttpRequest) -> HttpResponse:
    """
    Submit a web printing request. Returns a print code.
    """
    try:
        # user = logged_in_user(request)

        # with get_connection() as c:
        #     print_quota = get_quota(c, user)

        return HttpResponse({})

    except (KeyError, ValueError) as e:
        return HttpResponseBadRequest(e)
