import json
from enum import Enum
from functools import partial
from ipaddress import ip_address

from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from ipware import get_client_ip
from ocflib.infra.hosts import hosts_by_filter
from ocflib.infra.net import ipv4_to_ipv6
from ocflib.infra.net import is_ocf_ip
from ocflib.lab.stats import get_connection

from ocfweb.caching import cache

State = Enum('State', ['active', 'cleanup'])

get_connection = partial(
    get_connection,
    user=settings.OCFSTATS_USER,
    password=settings.OCFSTATS_PASSWORD,
    db=settings.OCFSTATS_DB,
)


@require_POST
@csrf_exempt
def log_session(request):
    """Primary API endpoint for session tracking.

    Desktops have a cronjob that calls this endpoint: https://git.io/vpIKX
    """

    remote_ip, _ = get_client_ip(request)

    if not is_ocf_ip(ip_address(remote_ip)):
        return HttpResponse('Not Authorized', status=401)

    try:
        host = _get_desktops().get(remote_ip)

        if not host:
            raise ValueError('IP {} does not belong to a desktop'.format(remote_ip))

        body = json.loads(request.body.decode('utf-8'))
        state = State[body.get('state')]  # triggers KeyError
        user = body.get('user')

        if state is State.cleanup or not user:
            # sessions also get periodically cleaned up: https://git.io/vpwg8
            _close_sessions(host)
        elif state is State.active and _session_exists(host, user):
            _refresh_session(host, user)
        else:
            _new_session(host, user)

        return HttpResponse(status=204)

    except (KeyError, ValueError) as e:
        return HttpResponseBadRequest(e)


def _new_session(host, user):
    """Register new session in when a user logs into a desktop."""

    _close_sessions(host)

    with get_connection() as c:
        c.execute(
            'INSERT INTO `session` (`host`, `user`, `start`, `last_update`) '
            'VALUES (%s, %s, NOW(), NOW())', (host, user),
        )


def _session_exists(host, user):
    """Returns whether an open session already exists for a given host and user."""

    with get_connection() as c:
        c.execute(
            'SELECT COUNT(*) AS `count` FROM `session` '
            'WHERE `host` = %s AND `user` = %s AND `end` IS NULL', (host, user),
        )

        return c.fetchone()['count'] > 0


def _refresh_session(host, user):
    """Keep a session around if the user is still logged in."""

    with get_connection() as c:
        c.execute(
            'UPDATE `session` SET `last_update` = NOW() '
            'WHERE `host` = %s AND `user` = %s AND `end` IS NULL', (host, user),
        )


def _close_sessions(host):
    """Close all sessions for a particular host."""

    with get_connection() as c:
        c.execute(
            'UPDATE `session` SET `end` = NOW(), `last_update` = NOW() '
            'WHERE `host` = %s AND `end` IS NULL', (host,),
        )


@cache(600)
def _get_desktops():
    """Return IPv4 and 6 address to fqdn mapping for OCF desktops from LDAP."""

    desktops = {}
    for e in hosts_by_filter('(type=desktop)'):
        host = e['cn'][0] + '.ocf.berkeley.edu'
        v4 = e['ipHostNumber'][0]
        v6 = ipv4_to_ipv6(ip_address(v4))
        desktops[v4] = host
        desktops[v6] = host
    return desktops
