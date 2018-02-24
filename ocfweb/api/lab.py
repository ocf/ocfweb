from django.http import JsonResponse
from ocflib.infra.hosts import hostname_from_domain
from ocflib.lab.stats import get_connection
from ocflib.lab.stats import list_desktops

from ocfweb.caching import cache
from ocfweb.caching import periodic


@cache()
def _enumerate_desktops():
    return list_desktops(public_only=True)


@periodic(15)
def _get_active_desktops():
    """List which desktops are currently in use."""

    # https://github.com/ocf/ocflib/blob/master/ocflib/lab/ocfstats.sql#L70
    # we don't use users_in_lab_count_public because we're looking for
    # desktops in use, and the view does COUNT(DISTINCT users)
    with get_connection() as c:
        c.execute(
            'SELECT `host` FROM `session_duration_public` '
            'WHERE `end` IS NULL;',
        )

    return {hostname_from_domain(i['host']) for i in c}


def desktop_usage(request):
    desktops = _enumerate_desktops()

    # get the list of public-only dekstops in use
    active_desktops = _get_active_desktops()
    desktops_in_use = active_desktops.intersection(desktops)

    return JsonResponse({
        'desktops_in_use': list(desktops_in_use),
        'total_desktops': len(desktops),
    })
