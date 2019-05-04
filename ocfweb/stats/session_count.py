import time
from datetime import date
from datetime import timedelta

from django.http import HttpResponse
from matplotlib.figure import Figure
from ocflib.lab.stats import get_connection

from ocfweb.caching import periodic
from ocfweb.component.graph import canonical_graph
from ocfweb.component.graph import current_start_end
from ocfweb.component.graph import plot_to_image_bytes


ONE_DAY = timedelta(days=1)


@periodic(60)
def _todays_session_image():
    return _sessions_image(*current_start_end())


@canonical_graph(hot_path=_todays_session_image)
def session_count_image(request, start_day, end_day):
    return _sessions_image(start_day, end_day)


def _sessions_image(start_day, end_day):
    return HttpResponse(
        plot_to_image_bytes(get_sessions_plot(start_day, end_day), format='svg'),
        content_type='image/svg+xml',
    )


def get_sessions_plot(start_day, end_day):
    """Return matplotlib plot representing unique sessions between start and
    end day.."""

    with get_connection() as c:
        query = '''
            SELECT `date`, `unique_logins`
            FROM `daily_sessions_public`
            WHERE `date` BETWEEN %s AND %s
        '''
        c.execute(query, (start_day, end_day))
        days = {r['date']: r for r in c}

    fig = Figure(figsize=(10, 3))
    ax = fig.add_subplot(1, 1, 1)

    x = []
    unique_logins = []

    day = start_day
    while day <= end_day:
        x.append(time.mktime(day.timetuple()))

        row = days.get(day)
        unique_logins.append(row['unique_logins'] if row else 0)

        day += ONE_DAY

    ax.grid(True)

    # we want to show an "o" marker to suggest the data points are discrete,
    # but it harms readability with too much data
    kwargs = {'marker': 'o'}
    if end_day - start_day > timedelta(days=60):
        del kwargs['marker']
    ax.plot(x, unique_logins, linewidth=2, **kwargs)

    ax.set_xlim(x[0], x[-1])

    skip = max(1, len(x) // 5)  # target 5 labels
    ax.set_xticks(x[::skip])
    ax.set_xticklabels(list(map(date.fromtimestamp, x))[::skip])
    ax.set_ylim(bottom=0)
    ax.set_title(
        'Unique lab logins {} to {}'.format(
            start_day.isoformat(),
            end_day.isoformat(),
        ),
    )
    return fig
