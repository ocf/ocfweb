from django.http import HttpResponse
from django.shortcuts import render
from matplotlib.figure import Figure
from ocflib.lab import stats
from ocflib.printing.quota import get_connection
from ocflib.printing.quota import SEMESTERLY_QUOTA

from ocfweb.caching import periodic
from ocfweb.component.graph import plot_to_image_bytes


def stats_printing(request):
    return render(
        request,
        'stats/printing.html',
        {
            'title': 'Printing Statistics',
            'toner_changes': _toner_changes(),
        },
    )


def semester_histogram(request):
    return HttpResponse(
        plot_to_image_bytes(_semester_histogram(), format='svg'),
        content_type='image/svg+xml',
    )


@periodic(300)
def _semester_histogram():
    with get_connection() as c:
        c.execute(
            'SELECT `user`, `semester` FROM `printed` WHERE `semester` > 0',
        )
        users = [SEMESTERLY_QUOTA - int(r['semester']) for r in c]

    fig = Figure(figsize=(10, 5))
    ax = fig.add_subplot(1, 1, 1)
    ax.locator_params(nbins=20)
    ax.hist(users, bins=list(range(0, 105, 5)))
    ax.grid(True)
    ax.set_xlim(SEMESTERLY_QUOTA, 0)
    ax.set_ylabel('Number of users')
    ax.set_xlabel('Remaining balance')
    ax.set_title('Remaining balances this semester')

    return fig


@periodic(3600)
def _toner_changes():
    return [
        (printer, _toner_changes_for_printer(printer))
        for printer in ('papercut', 'pagefault', 'logjam', 'deforestation')
    ]


def _toner_changes_for_printer(printer):
    with stats.get_connection() as cursor:
        cursor.execute('''
            CREATE TEMPORARY TABLE ordered1
                (PRIMARY KEY (position))
                AS (
                    SELECT * FROM (
                        SELECT
                            T.*,
                            @rownum := @rownum + 1 AS position
                            FROM (
                                (
                                    SELECT * FROM printer_toner_public
                                    WHERE printer = %s
                                    ORDER BY date
                                ) AS T,
                                (SELECT @rownum := 0) AS r
                            )
                    ) AS x
                )
        ''', (printer,))
        cursor.execute('''
            CREATE TEMPORARY TABLE ordered2
                (PRIMARY KEY (position))
                AS (SELECT * FROM ordered1)
        ''')
        cursor.execute('''
            SELECT
                B.date AS date,
                A.value as pages_before,
                B.value as pages_after
                FROM
                    ordered1 as A,
                    ordered2 as B
                WHERE
                    B.position = A.position + 1 AND
                    B.value > A.value AND
                    A.value > 0
        ''')
        return reversed(list(cursor))
