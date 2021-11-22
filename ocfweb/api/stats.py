from django.http import HttpRequest
from django.http import JsonResponse
from ocflib.lab.stats import humanize_bytes

from ocfweb.stats.mirrors import bandwidth_semester
from ocfweb.stats.summary import desktop_profiles
from ocfweb.stats.summary import printers
from ocfweb.stats.summary import staff_in_lab
from ocfweb.stats.summary import users_in_lab_count
from typing import List, Tuple
# These endpoints are for ocfstatic stats


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
    response = JsonResponse(
        printers(),
        safe=False,
    )
    return response


def get_desktop_usage(request: HttpRequest) -> JsonResponse:
    """
    Copy desktop usage from Django API by grabbing class attributes that
    can't be serialized to JSON
    """

    responseList = []
    for profile in desktop_profiles():
        minutes_idle = profile.minutes_idle
        minutes_busy = profile.minutes_busy
        responseList.append({
            'hostname': profile.hostname,
            'minutes_idle': int(minutes_idle),
            'minutes_busy': int(minutes_busy),
            'percent': int(100 * minutes_busy / max(1, (minutes_idle + minutes_busy))),
        })

    response = JsonResponse(
        responseList,
        safe=False,
    )
    return response


def get_mirrors_showcase(request: HttpRequest) -> JsonResponse:
    """ Return bandwidth for a few mirrors that we showcase on stats page
    In human-readable form, sorted with biggest bandwidth first
    """
    mirrors_showcase: List[Tuple[str, int]] = [('ubuntu', 0), ('debian', 0), ('archlinux', 0)]

    total, by_dist = bandwidth_semester(humanize=False)

    for m in mirrors_showcase:
        bw = 0
        for dist in by_dist:
            if dist[0].startswith(m[0]):
                bw += dist[1]
        m[1] = bw
    mirrors_showcase.sort(key=lambda m: m[1], reverse=True)
    response = JsonResponse(
        [[b[0], humanize_bytes(b[1])] for b in mirrors_showcase],
        safe=False,
    )

    return response
