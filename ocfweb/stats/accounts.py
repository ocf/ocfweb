import time
from collections import defaultdict
from datetime import date
from datetime import timedelta
from typing import Any
from typing import DefaultDict
from typing import Dict
from typing import Hashable
from typing import List

from django.http import HttpResponse
from django.shortcuts import render
from ocflib.infra.ldap import ldap_ocf
from ocflib.infra.ldap import OCF_LDAP_PEOPLE

from ocfweb.caching import cache


def stats_accounts(request: Any) -> HttpResponse:
    account_data = _get_account_stats()
    return render(
        request,
        'stats/accounts.html',
        {
            'title': 'Account Statistics',
            'total': [
                {
                    'name': 'Accounts',
                    'showInLegend': False,
                    'animation': False,
                    'data': account_data['cumulative_accounts'],
                },
            ],
            'group': [
                {
                    'name': 'Group Accounts',
                    'showInLegend': False,
                    'animation': False,
                    'data': account_data['cumulative_group_accounts'],
                },
            ],
        },
    )


@cache(ttl=600)
def _get_account_stats() -> Dict[str, List[Any]]:
    with ldap_ocf() as c:
        c.search(OCF_LDAP_PEOPLE, '(cn=*)', attributes=['creationTime', 'uidNumber', 'callinkOid'])
        response = c.response

    # Some accounts don't have creation times, so we assume that as UIDs
    # increase, so does time. We use this assumption to fill in the gaps.
    start_date = date(1995, 8, 21)
    last_creation_time = start_date
    sorted_accounts = sorted(response, key=lambda record: record['attributes']['uidNumber'])
    counts: DefaultDict[Hashable, int] = defaultdict(int)
    group_counts: DefaultDict[Hashable, int] = defaultdict(int)

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
        dates.append(time.mktime(cur.timetuple()) * 1000)

        cumulative_accounts.append(total)
        cumulative_group_accounts.append(group_total)

        cur += one_day
    return {
        'cumulative_accounts': list(zip(dates, cumulative_accounts)),
        'cumulative_group_accounts': list(zip(dates, cumulative_group_accounts)),
    }
