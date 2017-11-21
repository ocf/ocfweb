import json
from functools import partial

import pymysql
from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from ocflib.infra.ldap import ldap_ocf
from ocflib.infra.ldap import OCF_LDAP_HOSTS
from ocflib.lab.stats import get_connection

from ocfweb.caching import cache


def get_connection():
    return pymysql.connect(
        user=settings.OCFSTATS_USER,
        password=settings.OCFSTATS_PASSWORD,
        db=settings.OCFSTATS_DB,
        host='mysql.ocf.berkeley.edu',
        charset='utf8mb4',
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor,
    )

#get_connection = partial(get_connection, user='abizer', password=settings.OCFSTATS_PASSWORD, db='abizer')


@csrf_exempt
def desktop_checkin(request):
    """Primary API endpoint for session tracking.

    Desktops have a cronjob that calls this endpoint, replacing
    the functionality that used to be in ocf/labstats.
    """

    if request.method != 'POST':
        return HttpResponse('Not Authorized', status=401)

    try:
        body = json.loads(request.body.decode('utf-8'))

        host = body.get('host', _match_desktop(request.META['REMOTE_ADDR']))
        user = body['user']

        if _session_exists(host, user):
            _refresh_session(host, user)
        else:
            _new_session(host, user)

        return HttpResponse(status=200)

    except Exception as e:
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
    """Close old sessions for a particular host."""

    with get_connection() as c:
        c.execute(
            'UPDATE `session` SET `end` = NOW(), `last_update` = NOW() '
            'WHERE `host` = %s AND `end` IS NULL', (host,),
        )


def _match_desktop(ip):
    return _get_desktops()[ip]


@cache()
def _get_desktops():
    with ldap_ocf() as c:
        c.search(OCF_LDAP_HOSTS, '(type=desktop)', attributes=['cn', 'ipHostNumber'])
        return {e['attributes']['ipHostNumber'][0]: e['attributes']['cn'][0] + '.ocf.berkeley.edu' for e in c.response}
