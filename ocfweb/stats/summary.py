from datetime import date
from datetime import datetime
from operator import attrgetter

from django.shortcuts import render_to_response
from django.template import RequestContext
from ocflib.constants import CURRENT_SEMESTER_START
from ocflib.lab.printing import get_maintkit
from ocflib.lab.printing import get_toner
from ocflib.lab.printing import PRINTERS
from ocflib.lab.stats import list_desktops
from ocflib.lab.stats import staff_in_lab
from ocflib.lab.stats import STATS_EPOCH
from ocflib.lab.stats import top_staff_alltime
from ocflib.lab.stats import top_staff_semester
from ocflib.lab.stats import users_in_lab_count
from ocflib.lab.stats import UtilizationProfile

from ocfweb.stats.daily_graph import get_open_close


def summary(request):
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

    return render_to_response(
        'summary.html',
        {
            'title': 'Lab Statistics',
            'desktop_profiles': sorted(
                UtilizationProfile.from_hostnames(list_desktops(), open_, end).values(),
                key=attrgetter('hostname'),
            ),
            'current_semester_start': CURRENT_SEMESTER_START,
            'stats_epoch': STATS_EPOCH,
            'staff_in_lab': staff_in_lab(),
            'top_staff_alltime': top_staff_alltime()[:10],
            'top_staff_semester': top_staff_semester()[:10],
            'users_in_lab_count': users_in_lab_count(),
            'printers': sorted(
                (printer, get_toner(printer), get_maintkit(printer))
                for printer in PRINTERS
            ),
        },
        context_instance=RequestContext(request),
    )
