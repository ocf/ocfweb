from datetime import date

from django.shortcuts import render
from ocflib.lab.stats import current_semester_start
from ocflib.lab.stats import get_connection

from ocfweb.caching import periodic

MIRRORS_EPOCH = date(2017, 1, 1)


def stats_mirrors(request):
    return render(
        request,
        'stats/mirrors.html',
        {
            'title': 'Mirrors Statistics',
            'bandwidth_semester': bandwidth_semester(),
            'bandwidth_all_time': bandwidth_all_time(),
            'start_date': current_semester_start,
        },
    )

# TODO: move this to ocflib


def _humanize(n):
    # adapted from jvperrin/upload-to-box
    for unit in ['', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if n < 1024.0:
            return '{:3.2f} {}'.format(n, unit)
        n /= 1024.0


def _bandwidth_by_dist(start):
    with get_connection() as c:
        c.execute(
            'SELECT `dist`, SUM(`up` + `down`) as `bandwidth` FROM `mirrors_public` WHERE `date` > %s'
            'GROUP BY `dist` ORDER BY `bandwidth` DESC', start,
        )

    return [(i['dist'], _humanize(float(i['bandwidth']))) for i in c]


@periodic(86400)
def bandwidth_semester():
    return _bandwidth_by_dist(current_semester_start())


@periodic(86400)
def bandwidth_all_time():
    return _bandwidth_by_dist(MIRRORS_EPOCH)
