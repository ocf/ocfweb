from datetime import date
from datetime import datetime
from operator import attrgetter

from django.shortcuts import render
from ocflib.constants import CURRENT_SEMESTER_START
from ocflib.lab.printing import get_maintkit
from ocflib.lab.printing import get_toner
from ocflib.lab.printing import PRINTERS
from ocflib.lab.stats import list_desktops
from ocflib.lab.stats import staff_in_lab as real_staff_in_lab
from ocflib.lab.stats import STATS_EPOCH
from ocflib.lab.stats import top_staff_alltime as real_top_staff_alltime
from ocflib.lab.stats import top_staff_semester as real_top_staff_semester
from ocflib.lab.stats import users_in_lab_count as real_users_in_lab_count
from ocflib.lab.stats import UtilizationProfile

from ocfweb.caching import periodic
from ocfweb.stats.daily_graph import get_open_close


@periodic(60)
def desktop_profiles():
    open_, close = get_open_close(date.today())
    now = datetime.today()

    # If the lab has opened, but hasn't closed yet, only count
    # statistics until the current time. If the lab isn't open
    # yet, then don't count anything, and if it is closed, show
    # statistics from when it was open during the day.
    if now > open_ and now < close:
        end = now
    elif now <= open_:
        end = open_
    else:
        end = close

    return sorted(
        UtilizationProfile.from_hostnames(list_desktops(), open_, end).values(),
        key=attrgetter('hostname'),
    )


@periodic(30)
def staff_in_lab():
    return real_staff_in_lab()


@periodic(30)
def top_staff_alltime():
    return real_top_staff_alltime()


@periodic(30)
def top_staff_semester():
    return real_top_staff_semester()


@periodic(30)
def users_in_lab_count():
    return real_users_in_lab_count()


@periodic(60)
def printers():
    return sorted(
        (printer, get_toner(printer), get_maintkit(printer))
        for printer in PRINTERS
    )


def summary(request):
    return render(
        request,
        'summary.html',
        {
            'title': 'Lab Statistics',
            'desktop_profiles': desktop_profiles(),
            'current_semester_start': CURRENT_SEMESTER_START,
            'stats_epoch': STATS_EPOCH,
            'staff_in_lab': staff_in_lab(),
            'top_staff_alltime': top_staff_alltime()[:10],
            'top_staff_semester': top_staff_semester()[:10],
            'users_in_lab_count': users_in_lab_count(),
            'printers': printers(),
        },
    )
