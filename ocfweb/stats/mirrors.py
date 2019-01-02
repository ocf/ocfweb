from datetime import date

from django.shortcuts import render
from ocflib.lab.stats import bandwidth_by_dist
from ocflib.lab.stats import current_semester_start
from ocflib.lab.stats import humanize_bytes

from ocfweb.caching import periodic

MIRRORS_EPOCH = date(2017, 1, 1)


def stats_mirrors(request):

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
            'start_date': current_semester_start(),
        },
    )


@periodic(86400)
def bandwidth_semester():

    data = bandwidth_by_dist(current_semester_start())

    total = humanize_bytes(sum(x[1] for x in data))
    by_dist = [(dist, humanize_bytes(bw)) for dist, bw in data]

    return total, by_dist


@periodic(86400)
def bandwidth_all_time():

    data = bandwidth_by_dist(MIRRORS_EPOCH)

    total = humanize_bytes(sum(x[1] for x in data))
    by_dist = [(dist, humanize_bytes(bw)) for dist, bw in data]

    return total, by_dist
