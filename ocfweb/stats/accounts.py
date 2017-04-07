from collections import defaultdict
from datetime import date
from datetime import timedelta

from django.http import HttpResponse
from django.shortcuts import render
from matplotlib.dates import DateFormatter
from matplotlib.figure import Figure
from ocflib.infra.ldap import ldap_ocf
from ocflib.infra.ldap import OCF_LDAP_PEOPLE

from ocfweb.caching import cache
from ocfweb.caching import periodic
from ocfweb.component.graph import plot_to_image_bytes


def stats_accounts(request):
    return render(
        request,
        'stats/accounts.html',
        {
            'title': 'Account Statistics',
        },
    )


@cache(ttl=600)
def _get_account_stats():
    with ldap_ocf() as c:
        c.search(OCF_LDAP_PEOPLE, '(cn=*)', attributes=['creationTime', 'uidNumber', 'callinkOid'])
        response = c.response

    # Some accounts don't have creation times, so we assume that as UIDs
    # increase, so does time. We use this assumption to fill in the gaps.
    start_date = date(1989, 1, 1)
    last_creation_time = start_date
    sorted_accounts = sorted(response, key=lambda record: record['attributes']['uidNumber'])
    counts = defaultdict(int)
    group_counts = defaultdict(int)

    for account in sorted_accounts:
        creation_time = account['attributes'].get('creationTime', None)
        if creation_time:
            creation_time = creation_time.date()
            last_creation_time = creation_time
        else:
            creation_time = last_creation_time
        assert creation_time is not None

        counts[creation_time] += 1
        if isinstance(account['attributes']['callinkOid'], int):
            group_counts[creation_time] += 1

    one_day = timedelta(days=1)
    cur = start_date
    total = group_total = 0
    dates = []
    cumulative_accounts = []
    cumulative_group_accounts = []
    while cur <= date.today():
        total += counts[cur]
        group_total += group_counts[cur]
        dates.append(cur)

        cumulative_accounts.append(total)
        cumulative_group_accounts.append(group_total)

        cur += one_day

    return {
        'dates': dates,
        'cumulative_accounts': cumulative_accounts,
        'cumulative_group_accounts': cumulative_group_accounts,
    }


def cumulative_accounts_graph(request):
    """Graph of total cumulative accounts over time."""
    return HttpResponse(
        plot_to_image_bytes(_cumulative_accounts_graph(), format='svg'),
        content_type='image/svg+xml',
    )


@periodic(300)
def _cumulative_accounts_graph():
    stats = _get_account_stats()

    fig = Figure(figsize=(10, 5))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot_date(stats['dates'], stats['cumulative_accounts'], fmt='b-', color='b', linewidth=2.5)
    ax.xaxis.set_major_formatter(DateFormatter('%b %Y'))
    ax.grid(True)
    ax.set_ylabel('Number of accounts')
    ax.set_xlabel('Date')
    ax.set_title('Total OCF accounts')

    return fig


def cumulative_group_accounts_graph(request):
    """Graph of total cumulative group accounts over time."""
    return HttpResponse(
        plot_to_image_bytes(_cumulative_group_accounts_graph(), format='svg'),
        content_type='image/svg+xml',
    )


@periodic(300)
def _cumulative_group_accounts_graph():
    stats = _get_account_stats()

    fig = Figure(figsize=(10, 5))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot_date(
        stats['dates'],
        stats['cumulative_group_accounts'],
        fmt='b-',
        color='b',
        linewidth=2.5,
    )
    ax.xaxis.set_major_formatter(DateFormatter('%b %Y'))
    ax.grid(True)
    ax.set_ylabel('Number of group accounts')
    ax.set_xlabel('Date')
    ax.set_title('Total OCF group accounts')

    return fig
