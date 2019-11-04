from typing import Any

from django.http import JsonResponse

from ocfweb.main.staff_hours import get_staff_hours as real_get_staff_hours


def get_staff_hours(request: Any) -> JsonResponse:
    return JsonResponse(
        [item._asdict() for item in real_get_staff_hours()],
        safe=False,
    )
