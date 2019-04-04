from django.shortcuts import render
from ocflib.lab.stats import current_semester_start
from ocflib.lab.stats import SESSIONS_EPOCH
from ocflib.lab.stats import top_staff_alltime as real_top_staff_alltime
from ocflib.lab.stats import top_staff_semester as real_top_staff_semester

from ocfweb.caching import periodic


@periodic(300)
def top_staff_alltime():
    return real_top_staff_alltime()


@periodic(300)
def top_staff_semester():
    return real_top_staff_semester()


def session_stats(request):
    return render(
        request,
        'stats/session_stats.html',

        {
            'title': 'Session Statistics',
            'stats_epoch': SESSIONS_EPOCH,
            'current_semester_start': current_semester_start(),
            'top_staff_alltime': top_staff_alltime()[:15],
            'top_staff_semester': top_staff_semester()[:15],
        },
    )
