import ocflib.printing.quota as quota
from django.http import HttpResponse
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator
from ocflib.lab.stats import semester_dates
from ocflib.printing.quota import WEEKDAY_QUOTA
from ocflib.printing.quota import WEEKEND_QUOTA

from ocfweb.component.graph import canonical_graph
from ocfweb.component.graph import plot_to_image_bytes


@canonical_graph(default_start_end=semester_dates)
def weekday_jobs_image(request, start_day, end_day):
    return HttpResponse(
        plot_to_image_bytes(get_jobs_plot('weekday', start_day, end_day), format='svg'),
        content_type='image/svg+xml',
    )


@canonical_graph(default_start_end=semester_dates)
def weekend_jobs_image(request, start_day, end_day):
    return HttpResponse(
        plot_to_image_bytes(get_jobs_plot('weekend', start_day, end_day), format='svg'),
        content_type='image/svg+xml',
    )


# dictionary that gives parameters/config of different job graphs
graphs = {
    'weekday':
        {
            'query': '''
                SELECT `pages`, SUM(`count`) AS `count`
                FROM `public_jobs`
                WHERE
                    (`pages` <= %s) AND
                    (DAYOFWEEK(`day`) MOD 7 > 1) AND
                    (`day` BETWEEN CAST(%s AS Date) AND CAST(%s AS DATE))
                GROUP BY `pages`''',
            'quota': tuple([WEEKDAY_QUOTA]),
            'title': 'Semester Weekday Jobs Distributiom',
        },
    'weekend':
        {
            'query': '''
                SELECT `pages`, SUM(`count`) AS `count`
                FROM `public_jobs`
                WHERE
                    (`pages` <= %s) AND
                    (DAYOFWEEK(`day`) MOD 7 <= 1) AND
                    (`day` BETWEEN CAST(%s AS Date) AND CAST(%s AS DATE))
                GROUP BY `pages`''',
            'quota': tuple([WEEKEND_QUOTA]),
            'title': 'Semester Weekend Jobs Distribution',
        },
}


def freq_plot(
    data, title,
    ylab='Number of Jobs Printed',
):
    """takes in data, title, and ylab and makes a histogram, with
    the 1:len(data) as the xaxis
    """
    fig = Figure(figsize=(10, 4))
    ax = fig.add_subplot(1, 1, 1)

    tickLocations = range(1, len(data) + 1)
    width = 0.8
    ax.bar(tickLocations, data, width)

    ax.set_xticks(ticks=tickLocations)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.yaxis.grid(True)
    ax.set_ylim(ymin=0)
    ax.set_ylabel(ylab)
    ax.set_title(title)

    return fig


def get_jobs_plot(graph, start_day, end_day):
    """Return matplotlib plot of the number of jobs of different page-jobs"""
    graph_config = graphs[graph]
    with quota.get_connection() as cursor:
        cursor.execute(graph_config['query'],
                       graph_config['quota'] + (start_day, end_day))
        data = cursor.fetchall()

    jobs_dict = {row['pages']: row['count'] for row in data}
    jobs_count = [jobs_dict.get(i, 0) for i in range(1, graph_config['quota'][0] + 1)]

    return freq_plot(jobs_count, graph_config['title'])
