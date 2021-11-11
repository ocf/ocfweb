from django.http import HttpRequest
from django.http import JsonResponse

from ocfweb.stats.summary import staff_in_lab
from ocfweb.stats.summary import users_in_lab_count
from ocfweb.stats.summary import printers


def get_num_users_in_lab(request: HttpRequest) -> JsonResponse:
    return JsonResponse(
        users_in_lab_count(),
        safe=False,
    )


def get_staff_in_lab(request: HttpRequest) -> JsonResponse:
    return JsonResponse(
        staff_in_lab(),
        safe=False,
    )

def get_printers_summary(request: HttpRequest) -> JsonResponse:
    return JsonResponse(
        printers(),
        safe=False,
    )
