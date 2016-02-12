import pymysql
from django.http import HttpResponse
from django.shortcuts import render
from matplotlib.figure import Figure

from ocfweb.caching import periodic
from ocfweb.stats.plot import plot_to_image_bytes


# TODO: improve/move this after PyKota is gone
CURRENT_SEMESTER_QUOTA = 100


def pykota_connection(user='ocfpykota_user', password='not_a_secret'):
    return pymysql.connect(
        host='mysql.ocf.berkeley.edu',
        user=user,
        password=password,
        db='ocfpykota',
        cursorclass=pymysql.cursors.DictCursor,
    )


def stats_printing(request):
    return render(
        request,
        'printing.html',
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
    with pykota_connection() as c:
        c.execute(
            'SELECT GREATEST(0, `balance`) AS `balance` FROM `users` WHERE `balance` < %s',
            (CURRENT_SEMESTER_QUOTA,),
        )
        users = [r['balance'] for r in c]

    fig = Figure(figsize=(10, 5))
    ax = fig.add_subplot(1, 1, 1)
    ax.locator_params(nbins=20)
    ax.hist(users, bins=20)
    ax.grid(True)
    ax.set_xlim(CURRENT_SEMESTER_QUOTA, 0)
    ax.set_ylabel('Number of users')
    ax.set_xlabel('Remaining balance')
    ax.set_title('Remaining balances this semester')

    return fig
