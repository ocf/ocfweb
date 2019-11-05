import time
from collections import defaultdict
from datetime import date
from datetime import timedelta
from functools import partial
from typing import Any
from typing import Dict
from typing import List

from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render
from matplotlib.figure import Figure
from ocflib.lab import stats
from ocflib.printing.printers import PRINTERS
from ocflib.printing.quota import get_connection
from ocflib.printing.quota import SEMESTERLY_QUOTA

from ocfweb.caching import periodic
from ocfweb.component.graph import plot_to_image_bytes

ALL_PRINTERS = ('papercut', 'pagefault', 'logjam', 'logjam-old', 'deforestation')
ACTIVE_PRINTERS = ('papercut', 'pagefault', 'logjam')


def stats_printing(request: HttpRequest) -> HttpResponse:
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


def semester_histogram(request: HttpRequest) -> HttpResponse:
    return HttpResponse(
        plot_to_image_bytes(_semester_histogram(), format='svg'),
        content_type='image/svg+xml',
    )


@periodic(300)
def _semester_histogram() -> Figure:
    with get_connection() as c:
        c.execute(
            'SELECT `user`, `semester` FROM `printed` WHERE `semester` > 0',
        )
        users = [SEMESTERLY_QUOTA - int(r['semester']) for r in c]

    fig = Figure(figsize=(10, 5))
    ax = fig.add_subplot(1, 1, 1)
    ax.locator_params(nbins=20)
    ax.hist(users, bins=list(range(0, SEMESTERLY_QUOTA + 5, 5)))
    ax.grid(True)
    ax.set_xlim(SEMESTERLY_QUOTA, 0)
    ax.set_ylabel('Number of users')
    ax.set_xlabel('Remaining balance')
    ax.set_title('Remaining balances this semester')

    return fig


@periodic(3600)
def _toner_changes() -> List[Any]:
    return [
        (
            printer,
            _toner_used_by_printer(printer),
        )
        for printer in ACTIVE_PRINTERS
    ]


def _toner_used_by_printer(printer: str, cutoff: float = .05, since: date = stats.current_semester_start()) -> float:
    """Returns toner used for a printer since a given date (by default it
    returns toner used for this semester).

    Toner numbers can be significantly noisy, including significant diffs
    whenever toner gets taken out and put back in whenever there is a jam.
    Because of this it's hard to determine if a new toner is inserted into a
    printer or if it was the same toner again. To reduce this noise we only
    count diffs that are smaller than a cutoff which empirically seems to be
    more accurate.
    """
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
        ''', (cutoff,),
        )
        result = cursor.fetchone()['toner_used']
        return float(result or 0.0)


@periodic(120)
def _pages_per_day() -> Dict[str, int]:
    with stats.get_connection() as cursor:
        cursor.execute('''
            SELECT max(value) as value, cast(date as date) as date, printer
                FROM printer_pages_public
                GROUP BY cast(date as date), printer
                ORDER BY date ASC, printer ASC
        ''')

        # Resolves the issue of possible missing dates.
        # defaultdict(lambda: defaultdict(int)) doesn't work due to inability to pickle local objects like lambdas;
        # this effectively does the same thing as that.
        pages_printed: Dict[Any, Any] = defaultdict(partial(defaultdict, int))
        last_seen: Dict[Any, Any] = {}

        for row in cursor:
            if row['printer'] in last_seen:
                pages_printed.setdefault(row['date'], defaultdict(int))
                pages_printed[row['date']][row['printer']] = (
                    row['value'] - last_seen[row['printer']]
                )
            last_seen[row['printer']] = row['value']

    return pages_printed


def _pages_printed_for_printer(printer: str, resolution: int = 100) -> List[Any]:
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
def _pages_printed_data() -> List[Any]:
    return [
        {
            'name': printer,
            'animation': False,
            'data': _pages_printed_for_printer(printer),
        }
        for printer in ALL_PRINTERS
    ]


def pages_printed(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        'stats/printing/pages-printed.html',
        {
            'title': 'Pages Printed',
            'data': _pages_printed_data(),
        },
    )
