import time
from collections import defaultdict
from datetime import date
from datetime import timedelta

from django.http import HttpResponse
from django.shortcuts import render
from matplotlib.figure import Figure
from ocflib.lab import stats
from ocflib.printing.printers import PRINTERS
from ocflib.printing.quota import get_connection
from ocflib.printing.quota import SEMESTERLY_QUOTA

from ocfweb.caching import periodic
from ocfweb.component.graph import plot_to_image_bytes


ALL_PRINTERS = ('papercut', 'pagefault', 'logjam', 'deforestation')


def stats_printing(request):
    return render(
        request,
        'stats/printing.html',
        {
            'title': 'Printing Statistics',
            'current_printers': PRINTERS,
            'toner_changes': _toner_changes(),
            'last_month': [
                date.today() - timedelta(days=i)
                for i in range(30)
            ],
            'pages_per_day': _pages_per_day(),
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
        for printer in ALL_PRINTERS
    ]


# Toner numbers can be significantly noisy, including significant diffs
# whenever toner gets taken out and put back in whenever there is jam. Because
# of this it's hard to determine if a new toner is inserted into a printer to
# reduce this noise we only count diffs that are smaller than a cutoff which
# empirically seems to be more accurate
def _toner_used_by_printer(printer, cutoff=.05, since=date(2017, 8, 20)):
    with stats.get_connection() as cursor:
        cursor.execute(
            '''
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
                                    WHERE printer = %s AND
                                    date > %s
                                    ORDER BY date
                                ) AS T,
                                (SELECT @rownum := 0) AS r
                            )
                    ) AS x
                )
        ''', (printer, since.strftime('%Y-%m-%d')),
        )
        cursor.execute('''
            CREATE TEMPORARY TABLE ordered2
                (PRIMARY KEY (position))
                AS (SELECT * FROM ordered1)
        ''')
        cursor.execute('''
            CREATE TEMPORARY TABLE diffs
            AS (SELECT
                B.date AS date,
                A.value/A.max - B.value/B.max as pct_diff
                FROM
                    ordered1 as A,
                    ordered2 as B
                WHERE
                    B.position = A.position + 1)
        ''')
        cursor.execute(
            '''
            SELECT SUM(pct_diff) as toner_used
            FROM
            diffs
            WHERE
            ABS(pct_diff)<%s
        ''', (cutoff),
        )
        return float(cursor.fetchone()['toner_used'])


@periodic(120)
def _pages_per_day():
    with stats.get_connection() as cursor:
        cursor.execute('''
            SELECT max(value) as value, cast(date as date) as date, printer
                FROM printer_pages_public
                GROUP BY cast(date as date), printer
                ORDER BY date ASC, printer ASC
        ''')

        last_seen = {}
        pages_printed = {}

        for row in cursor:
            if row['printer'] in last_seen:
                pages_printed.setdefault(row['date'], defaultdict(int))
                pages_printed[row['date']][row['printer']] = (
                    row['value'] - last_seen[row['printer']]
                )
            last_seen[row['printer']] = row['value']

    return pages_printed


def _toner_changes_for_printer(printer):
    with stats.get_connection() as cursor:
        cursor.execute(
            '''
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
        ''', (printer,),
        )
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
           LIMIT 20;
        ''')
        return reversed(list(cursor))


def _pages_printed_for_printer(printer, resolution=100):
    with stats.get_connection() as cursor:
        cursor.execute(
            '''
            SELECT Z.date, Z.value FROM (
                SELECT
                    T.*,
                    @rownum := @rownum + 1 AS position
                FROM (
                    (
                        SELECT * FROM printer_pages_public
                        WHERE printer = %s
                        ORDER BY date
                    ) AS T,
                    (SELECT @rownum := 0) AS r
                )
            ) as Z
            WHERE Z.position mod %s = 0
        ''', (printer, resolution),
        )
        return [
            (time.mktime(row['date'].timetuple()) * 1000, row['value'])
            for row in cursor
        ]


@periodic(3600)
def _pages_printed_data():
    return [
        {
            'name': printer,
            'animation': False,
            'data': _pages_printed_for_printer(printer),
        }
        for printer in ALL_PRINTERS
    ]


def pages_printed(request):
    return render(
        request,
        'stats/printing/pages-printed.html',
        {
            'title': 'Pages Printed',
            'data': _pages_printed_data(),
        },
    )
