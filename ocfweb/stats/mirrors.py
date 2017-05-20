from datetime import date

from django.shortcuts import render
from humanize import naturalsize
from ocflib.lab.stats import current_semester_start
from ocflib.lab.stats import get_connection

MIRRORS_EPOCH = date(2017, 1, 1)


def stats_mirrors(request):
    return render(
        request,
        'stats/mirrors.html',
        {
            'title': 'Mirrors Statistics',
            'bandwidth_semester': bandwidth_by_dist(),
            'bandwidth_all_time': bandwidth_by_dist(MIRRORS_EPOCH),
            'start_date': current_semester_start,
        }
    )


def bandwidth_by_dist(start=current_semester_start()):
    with get_connection() as c:
        c.execute(
            'SELECT `dist`, SUM(`up` + `down`) as `bandwidth` FROM `mirrors_public` WHERE `date` > %s'
            'GROUP BY `dist` ORDER BY `bandwidth` DESC', (start))

    return [(i['dist'], naturalsize(i['bandwidth'])) for i in c]
