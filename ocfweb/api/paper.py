from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from ocflib.printing.quota import get_connection
from ocflib.printing.quota import get_quota

from ocfweb.auth import login_required
from ocfweb.component.session import logged_in_user


@require_POST
@login_required
def paper_quota(request: HttpRequest) -> HttpResponse:
    try:
        user = logged_in_user(request)

        with get_connection() as c:
            quota = get_quota(c, user)
            print(type(quota))
            return JsonResponse({
                'user': quota.user,
                'daily': quota.daily,
                'semesterly': quota.semesterly,
            })

    except (KeyError, ValueError) as e:
        return HttpResponseBadRequest(e)
