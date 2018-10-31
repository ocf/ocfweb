from django.http import JsonResponse
from ocflib.infra.hosts import hostname_from_domain
from ocflib.lab.stats import get_connection
from ocflib.lab.stats import list_desktops

from ocfweb.caching import cache
from ocfweb.caching import periodic


@cache()
def _list_public_desktops():
    return list_desktops(public_only=True)


@periodic(5)
def _get_desktops_in_use():
    """List which desktops are currently in use."""

    # https://github.com/ocf/ocflib/blob/90f9268a89ac9d53c089ab819c1aa95bdc38823d/ocflib/lab/ocfstats.sql#L70
    # we don't use users_in_lab_count_public because we're looking for
    # desktops in use, and the view does COUNT(DISTINCT users)
    with get_connection() as c:
        c.execute(
            'SELECT * FROM `desktops_in_use_public`;',
        )

    return {hostname_from_domain(session['host']) for session in c}


def desktop_usage(request):
    public_desktops = _list_public_desktops()

    desktops_in_use = _get_desktops_in_use()
    public_desktops_in_use = desktops_in_use.intersection(public_desktops)

    return JsonResponse({
        'public_desktops_in_use': list(public_desktops_in_use),
        'public_desktops_num': len(public_desktops),
    })
