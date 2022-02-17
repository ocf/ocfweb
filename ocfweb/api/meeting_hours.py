from django.http import HttpRequest
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from ocflib.org.meeting_hours import read_current_meeting
from ocflib.org.meeting_hours import read_meeting_list
from ocflib.org.meeting_hours import read_next_meeting


def get_meetings_list(request: HttpRequest) -> JsonResponse:
    return JsonResponse(
        [item._asdict() for item in read_meeting_list()],
        safe=False,
    )


@never_cache
def get_next_meeting(request: HttpRequest) -> JsonResponse:
    next_meeting = read_next_meeting()
    if next_meeting is None:
        return JsonResponse(
            {},
            status=204,
        )

    return JsonResponse(
        next_meeting._asdict(),
        safe=False,
    )


@never_cache
def get_current_meeting(request: HttpRequest) -> JsonResponse:
    current_meeting = read_current_meeting()
    if current_meeting is None:
        return JsonResponse(
            {},
            status=204,
        )

    return JsonResponse(
        current_meeting._asdict(),
        safe=False,
    )
