import urllib.parse
from datetime import date
from datetime import datetime
from datetime import timedelta

import numpy as np
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect
from matplotlib.figure import Figure
from ocflib.lab.hours import Day
from ocflib.lab.stats import list_desktops
from ocflib.lab.stats import UtilizationProfile

from ocfweb.caching import periodic
from ocfweb.stats.plot import plot_to_image_bytes


# Binomial-shaped weights for moving average
AVERAGE_WEIGHTS = tuple(zip(range(-2, 3), (n / 16 for n in (1, 4, 6, 4, 1))))


@periodic(60)
def _daily_graph_image(day=None):
    if not day:
        day = date.today()

    return HttpResponse(
        plot_to_image_bytes(get_daily_plot(day), format='svg'),
        content_type='image/svg+xml',
    )


def daily_graph_image(request):
    try:
        day = datetime.strptime(request.GET.get('date', ''), '%Y-%m-%d').date()
    except ValueError:
        day = date.today()

    # redirect to canonical url
    if request.GET.get('date') != day.isoformat():
        return redirect('{}?{}'.format(
            reverse('daily_graph_image'),
            urllib.parse.urlencode({'date': day.isoformat()}),
        ))

    if day == date.today():
        return _daily_graph_image()
    else:
        return _daily_graph_image(day=day)


def get_open_close(day):
    """Return datetime objects representing open and close for a day.

    If the lab is closed all day (e.g. holiday), we just return midnight of the
    current and next day (i.e. all 24 hours).
    """
    d = Day.from_date(day)

    if not d.closed_all_day:
        start = datetime(day.year, day.month, day.day, min(h.open for h in d.hours))
        end = datetime(day.year, day.month, day.day, max(h.close for h in d.hours))
    else:
        start = datetime(day.year, day.month, day.day)
        end = start + timedelta(days=1)

    return start, end


# TODO: caching; we can cache for a long time if it's a day that's already happened
def get_daily_plot(day):
    """Return matplotlib plot representing a day's plot."""
    start, end = get_open_close(day)
    profiles = UtilizationProfile.from_hostnames(list_desktops(public_only=True), start, end).values()

    minutes = int((end - start).total_seconds() // 60)
    now = datetime.now()
    if now >= end or now <= start:
        now = None
    minute_now = None if not now else int((now - start).total_seconds() // 60)
    sums = []

    for minute in range(minutes):
        instant15 = start + timedelta(minutes=minute, seconds=15)
        instant45 = start + timedelta(minutes=minute, seconds=45)
        in_use = sum(1 if profile.in_use(instant15)
                     or profile.in_use(instant45) else 0 for profile in profiles)
        sums.append(in_use)

    # Do a weighted moving average to smooth out the data
    processed = [0] * len(sums)
    for i in range(len(sums)):
        for delta_i, weight in AVERAGE_WEIGHTS:
            m = i if (i + delta_i < 0 or i + delta_i >= len(sums)) else i + delta_i
            # Don't use data that hasn't occurred yet
            if minute_now and i <= minute_now and m >= minute_now:
                processed[i] += weight * sums[i]
            elif minute_now and i > minute_now:
                processed[i] = 0
            else:
                processed[i] += weight * sums[m]
    h = lambda h: h if h <= 12 else h - 12
    p = lambda h: 'am' if h <= 11 else 'pm'
    hours = ['{}{}'.format(h(hour), p(hour)) for hour in range(start.hour, start.hour + minutes // 60)]

    fig = Figure(figsize=(10, 6))
    ax = fig.add_subplot(1, 1, 1)

    x = list(range(minutes))
    ax.grid(True)
    ax.plot(x, processed, color='k', linewidth=1.5)

    # Draw a vertical line, if applicable, showing current time
    if minute_now:
        ax.axvline(minute_now, linewidth=1.5)

    ax.set_xlim(0, minutes)
    ax.set_xticks(np.arange(0, minutes, 60), hours)
    ax.set_xlabel('Time')
    ax.set_ylim(0, len(profiles))
    ax.set_ylabel('Computers in Use')

    ax.set_title('Lab Utilization {}'.format(day.strftime('%a %b %d, %Y')))
    return fig
