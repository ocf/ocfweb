import time
from datetime import date
from datetime import timedelta

from django.http import HttpResponse
from matplotlib.figure import Figure
from ocflib.lab.stats import get_connection

from ocfweb.caching import periodic
from ocfweb.component.graph import canonical_graph
from ocfweb.component.graph import plot_to_image_bytes


DEFAULT_DAYS = 90
ONE_DAY = timedelta(days=1)


def current_start_end():
    """Return current default start and end date."""
    end = date.today()
    return end - timedelta(days=DEFAULT_DAYS), end


@periodic(60)
def _todays_session_image():
    return _sessions_image(*current_start_end())


@canonical_graph(hot_path=_todays_session_image)
def session_length_image(request, start_day, end_day):
    return _sessions_image(start_day, end_day)


def _sessions_image(start_day, end_day):
    return HttpResponse(
        plot_to_image_bytes(get_sessions_plot(start_day, end_day), format='svg'),
        content_type='image/svg+xml',
    )


def get_sessions_plot(start_day, end_day):
    """Return matplotlib plot representing median session length between start
    and end day.."""

    with get_connection() as c:
        query = '''
        SELECT
            CAST(start AS DATE) AS date,
            AVG(TIME_TO_SEC(duration)) as mean_duration_seconds
          FROM session_duration_public
          WHERE
            start BETWEEN %s AND %s
            AND end IS NOT NULL
          GROUP BY date
        '''
        c.execute(query, (start_day, end_day))
        days = {r['date']: r for r in c}

    fig = Figure(figsize=(10, 3))
    ax = fig.add_subplot(1, 1, 1)

    x = []
    mean_duration_hours = []

    day = start_day
    while day <= end_day:
        x.append(time.mktime(day.timetuple()))

        row = days.get(day)
        mean_duration_hours.append(row['mean_duration_seconds'] / 3600 if row else 0)

        day += ONE_DAY

    ax.grid(True)

    # we want to show an "o" marker to suggest the data points are discrete,
    # but it harms readability with too much data
    kwargs = {'marker': 'o'}
    if end_day - start_day > timedelta(days=60):
        del kwargs['marker']
    ax.plot(x, mean_duration_hours, linewidth=2, **kwargs)

    ax.set_xlim(x[0], x[-1])

    skip = max(1, len(x) // 5)  # target 5 labels
    ax.set_xticks(x[::skip])
    ax.set_xticklabels(list(map(date.fromtimestamp, x))[::skip])
    ax.set_ylim(ymin=0)
    ax.set_ylabel('Duration (hours)')
    ax.set_title('Mean session duration {} to {}'.format(
        start_day.isoformat(),
        end_day.isoformat(),
    ))
    return fig
