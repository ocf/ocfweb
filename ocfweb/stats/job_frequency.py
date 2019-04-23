import urllib.parse
from datetime import date
from datetime import datetime

import numpy as np
import ocflib.printing.quota as quota
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator

from ocfweb.caching import periodic
from ocfweb.component.graph import plot_to_image_bytes


def pyday_to_sqlday(pyday):
    """Converting weekday index from python to mysql."""
    return (pyday + 1) % 7 + 1


@periodic(1800)
def _jobs_graph_image(day=None):
    if not day:
        day = date.today()

    return HttpResponse(
        plot_to_image_bytes(get_jobs_plot(day), format='svg'),
        content_type='image/svg+xml',
    )


def daily_jobs_image(request):
    try:
        day = datetime.strptime(request.GET.get('date', ''), '%Y-%m-%d').date()
    except ValueError:
        day = date.today()

    # redirect to canonical url
    if request.GET.get('date') != day.isoformat():
        return redirect('{}?{}'.format(
            reverse('daily_job_image'),
            urllib.parse.urlencode({'date': day.isoformat()}),
        ))

    if day == date.today():
        return _jobs_graph_image()
    else:
        return _jobs_graph_image(day=day)


def get_jobs_plot(day):
    """Return matplotlib plot showing the number i-page-job to the day."""

    day_of_week = pyday_to_sqlday(day.weekday())
    day_quota = quota.daily_quota(datetime.combine(day, datetime.min.time()))

    sql_today_freq = '''
    SELECT `pages`,  SUM(`count`) AS `count`
    FROM `public_jobs`
    WHERE
        (`pages` <= %s) AND
        (DAYOFWEEK(`day`) = %s) AND
        (`day` = %s )
    GROUP BY `pages`
    ORDER BY `pages` ASC
    '''

    # executing the sql query to get the data
    with quota.get_connection() as cursor:
        cursor.execute(sql_today_freq, (day_quota, day_of_week, day))
        today_freq_data = cursor.fetchall()

    # converting the data into a list
    today_jobs_dict = {row['pages']: row['count'] for row in today_freq_data}
    today_jobs_count = [today_jobs_dict.get(i, 0) for i in range(1, day_quota + 1)]

    # Generating the plot
    fig = Figure(figsize=(10, 4))
    ax = fig.add_subplot(1, 1, 1)

    tickLocations = np.arange(1, day_quota + 1)
    width = 0.8
    ax.bar(tickLocations, today_jobs_count, width)

    ax.set_xticks(ticks=tickLocations)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.yaxis.grid(True)
    ax.set_ylim(bottom=0)
    ax.set_ylabel('Number of Jobs Printed')
    ax.set_title(f'Print Job Distribution {day:%a %b %d}')

    return fig
