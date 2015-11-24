from datetime import date

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
            'desktop_profiles': [
                UtilizationProfile.from_hostname(desktop, open_, close)
                for desktop in sorted(list_desktops())
            ],
        },
        context_instance=RequestContext(request),
    )
