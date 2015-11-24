from datetime import date
from operator import attrgetter

from django.shortcuts import render_to_response
from django.template import RequestContext
from ocflib.lab.stats import list_desktops
from ocflib.lab.stats import UtilizationProfile

from ocfweb.stats.daily_graph import get_open_close


def summary(request):
    open_, close = get_open_close(date.today())

    return render_to_response(
        'summary.html',
        {
            'title': 'Lab Statistics',
            'desktop_profiles': sorted(
                UtilizationProfile.from_hostnames(list_desktops(), open_, close).values(),
                key=attrgetter('hostname'),
            ),
        },
        context_instance=RequestContext(request),
    )
