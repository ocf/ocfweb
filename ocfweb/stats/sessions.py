import time
import urllib.parse
from datetime import date
from datetime import datetime
from datetime import timedelta

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect
from matplotlib.figure import Figure
from ocflib.lab.stats import get_connection

from ocfweb.caching import periodic
from ocfweb.stats.plot import plot_to_image_bytes


DEFAULT_DAYS = 14
MIN_DAYS = 1
MAX_DAYS = 365 * 5
ONE_DAY = timedelta(days=1)


def current_start_end():
    """Return current default start and end date."""
    end = date.today()
    return end - timedelta(days=DEFAULT_DAYS), end


@periodic(60)
def _todays_session_image():
    return _sessions_image(*current_start_end())


def _sessions_image(start_day, end_day):
    return HttpResponse(
        plot_to_image_bytes(get_sessions_plot(start_day, end_day), format='svg'),
        content_type='image/svg+xml',
    )


def sessions_image(request):
    def get_day_from_params(param, default):
        try:
            return datetime.strptime(request.GET.get(param, ''), '%Y-%m-%d').date()
        except ValueError:
            return default

    default_start, default_end = current_start_end()

    start_day = get_day_from_params('start', default_start)
    end_day = get_day_from_params('end', default_end)

    if end_day <= start_day:
        return HttpResponse(
            'end_day must be after start_day',
            status=400,
        )

    # redirect to canonical url
    if (
            request.GET.get('start') != start_day.isoformat() or
            request.GET.get('end') != end_day.isoformat()
    ):
        return redirect('{}?{}'.format(
            reverse('sessions_image'),
            urllib.parse.urlencode({
                'start': start_day.isoformat(),
                'end': end_day.isoformat(),
            }),
        ))

    if start_day == default_start and end_day == default_end:
        # hot path: cached image
        return _todays_session_image()
    else:
        return _sessions_image(start_day, end_day)


def get_sessions_plot(start_day, end_day):
    """Return matplotlib plot representing unique sessions between start and
    end day.."""

    with get_connection() as c:
        query = '''
            SELECT `date`, `logins`, `unique_logins`
            FROM `daily_sessions_public`
            WHERE `date` BETWEEN %s AND %s
        '''
        c.execute(query, (start_day, end_day))
        days = {r['date']: r for r in c}

    fig = Figure(figsize=(10, 3))
    ax = fig.add_subplot(1, 1, 1)

    x = []
    logins = []
    unique_logins = []

    day = start_day
    while day <= end_day:
        x.append(time.mktime(day.timetuple()))

        row = days.get(day)
        if row:
            logins.append(row['logins'])
            unique_logins.append(row['unique_logins'])
        else:
            logins.append(0)
            unique_logins.append(0)

        day += ONE_DAY

    ax.grid(True)
    ax.plot(x, logins, color='b', marker='o', linewidth=1.5, label='Logins')
    ax.plot(x, unique_logins, color='r', marker='o', linewidth=2, label='Unique Logins')
    ax.set_xlim(x[0], x[-1])

    skip = max(1, len(x) // 5)  # target 5 labels
    ax.set_xticks(x[::skip])
    ax.set_xticklabels(list(map(date.fromtimestamp, x))[::skip])
    ax.set_ylim(ymin=0)
    ax.legend(loc='best', shadow=True)
    ax.set_title('Lab sessions {} to {}'.format(
        start_day.isoformat(),
        end_day.isoformat(),
    ))
    return fig
