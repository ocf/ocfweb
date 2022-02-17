from typing import Any
from typing import List

from django.http import HttpRequest
from django.http import JsonResponse
from ocflib.org.meeting_hours import read_current_meeting
from ocflib.org.meeting_hours import read_meeting_list
from ocflib.org.meeting_hours import read_next_meeting

from ocfweb.caching import periodic


def get_meetings_list(request: HttpRequest) -> JsonResponse:
    return JsonResponse(
        [item._asdict() for item in _read_meeting_list()],
        safe=False,
    )


def get_next_meeting(request: HttpRequest) -> JsonResponse:
    next_meeting = _read_next_meeting()
    if next_meeting is None:
        return JsonResponse(
            {},
            status=204,
        )

    return JsonResponse(
        next_meeting._asdict(),
        safe=False,
    )


def get_current_meeting(request: HttpRequest) -> JsonResponse:
    current_meeting = _read_current_meeting()
    if current_meeting is None:
        return JsonResponse(
            {},
            status=204,
        )

    return JsonResponse(
        current_meeting._asdict(),
        safe=False,
    )


def _read_meeting_list() -> List[Any]:
    return read_meeting_list()


@periodic(5)
def _read_next_meeting() -> List[Any]:
    return read_next_meeting()


@periodic(5)
def _read_current_meeting() -> List[Any]:
    return read_current_meeting()
