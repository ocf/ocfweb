from datetime import date
from typing import Any
from typing import Tuple

from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render
from ocflib.lab.stats import bandwidth_by_dist
from ocflib.lab.stats import current_semester_start
from ocflib.lab.stats import humanize_bytes

from ocfweb.caching import periodic

MIRRORS_EPOCH = date(2017, 1, 1)
MIRRORS_REPORTING_FIXED = date(2021, 10, 11)


def stats_mirrors(request: HttpRequest) -> HttpResponse:

    semester_total, semester_dists = bandwidth_semester()
    all_time_total, all_time_dists = bandwidth_all_time()

    return render(
        request,
        'stats/mirrors.html',
        {
            'title': 'Mirrors Statistics',
            'semester_total': semester_total,
            'semester_dists': semester_dists,
            'all_time_total': all_time_total,
            'all_time_dists': all_time_dists,
            'start_date': current_semester_start() if (
                current_semester_start() > MIRRORS_REPORTING_FIXED
            ) else MIRRORS_REPORTING_FIXED,
        },
    )


@periodic(86400)
def bandwidth_semester() -> Tuple[Any, Any]:
    if current_semester_start() > MIRRORS_REPORTING_FIXED:
        data = bandwidth_by_dist(current_semester_start())
    else:
        data = bandwidth_by_dist(MIRRORS_REPORTING_FIXED)

    total = humanize_bytes(sum(x[1] for x in data))
    by_dist = [(dist, humanize_bytes(bw)) for dist, bw in data]

    return total, by_dist


@periodic(86400)
def bandwidth_all_time() -> Tuple[Any, Any]:

    data = bandwidth_by_dist(MIRRORS_EPOCH)

    total = humanize_bytes(sum(x[1] for x in data))
    by_dist = [(dist, humanize_bytes(bw)) for dist, bw in data]

    return total, by_dist
