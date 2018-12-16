import logging
from datetime import date
from datetime import datetime
from operator import attrgetter

from django.shortcuts import render
from ocflib.lab.stats import current_semester_start
from ocflib.lab.stats import list_desktops
from ocflib.lab.stats import SESSIONS_EPOCH
from ocflib.lab.stats import staff_in_lab as real_staff_in_lab
from ocflib.lab.stats import staff_in_lab_count as real_staff_in_lab_count
from ocflib.lab.stats import top_staff_alltime as real_top_staff_alltime
from ocflib.lab.stats import top_staff_semester as real_top_staff_semester
from ocflib.lab.stats import users_in_lab_count as real_users_in_lab_count
from ocflib.lab.stats import UtilizationProfile
from ocflib.printing.printers import get_maintkit
from ocflib.printing.printers import get_toner
from ocflib.printing.printers import PRINTERS

from ocfweb.caching import periodic
from ocfweb.stats.daily_graph import get_open_close


_logger = logging.getLogger(__name__)


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


@periodic(300)
def top_staff_alltime():
    return real_top_staff_alltime()


@periodic(300)
def top_staff_semester():
    return real_top_staff_semester()


@periodic(30)
def users_in_lab_count():
    return real_users_in_lab_count()


@periodic(30)
def staff_in_lab_count():
    return real_staff_in_lab_count()


@periodic(60)
def printers():
    def silence(f):
        def inner(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except (OSError, ValueError) as ex:
                _logger.warn('Silencing exception reading printer data: {}'.format(ex))
                return None
        return inner

    return sorted(
        (printer, silence(get_toner)(printer), silence(get_maintkit)(printer))
        for printer in PRINTERS
    )


def summary(request):
    return render(
        request,
        'stats/summary.html',
        {
            'title': 'Lab Statistics',
            'desktop_profiles': desktop_profiles(),
            'current_semester_start': current_semester_start(),
            'stats_epoch': SESSIONS_EPOCH,
            'staff_in_lab': staff_in_lab(),
            'top_staff_alltime': top_staff_alltime()[:15],
            'top_staff_semester': top_staff_semester()[:15],
            'users_in_lab_count': users_in_lab_count(),
            'staff_in_lab_count': staff_in_lab_count(),
            'printers': printers(),
        },
    )
