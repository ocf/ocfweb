from django.http import HttpResponse
from django.shortcuts import render
from matplotlib.figure import Figure
from ocflib.printing.quota import get_connection
from ocflib.printing.quota import SEMESTERLY_QUOTA

from ocfweb.caching import periodic
from ocfweb.stats.plot import plot_to_image_bytes


def stats_printing(request):
    return render(
        request,
        'stats/printing.html',
        {
            'title': 'Printing Statistics',
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
