# TODO: rename this to some generic ocfweb config file, since it's not just for
# lab status anymore
from collections import namedtuple

import requests
import yaml
from django.shortcuts import render

from ocfweb.account.constants import TESTER_CALNET_UIDS
from ocfweb.caching import periodic


LabStatus = namedtuple('LabStatus', (
    'force_lab_closed',
    'banner_html',
    'create_disabled',
))


@periodic(60, ttl=86400)
def get_lab_status():
    """Load the lab status from the default location."""
    try:
        with open('/home/s/st/staff/lab_status.yaml') as f:
            status = yaml.safe_load(f)
    except IOError:
        req = requests.get('https://www.ocf.berkeley.edu/~staff/lab_status.yaml')
        assert req.status_code == 200, req.status_code
        status = yaml.safe_load(req.text)
    return LabStatus(
        force_lab_closed=status['force_lab_closed'],
        banner_html=status.get('banner_html', ''),
        create_disabled=status['create_disabled'],
    )


def create_required(fn):
    """Mark a view as requiring create.

    The view will be disabled (non-staff users will get a 503) when
    create_disabled is specified in lab_status.yaml.

    The purpose of this is so that we can disable create when things are broken
    (or when we're testing), which gives users a reasonable error. This is
    nicer than the alternative (random 500s after they've filled out the entire
    form).

    Staff are exempted based on calnet testers.
    """
    def _decorator(request, *args, **kwargs):
        lab_status = get_lab_status()

        if lab_status.create_disabled:
            calnet_uid = request.session.get('calnet_uid')
            if calnet_uid not in TESTER_CALNET_UIDS:
                return render(request, 'create_disabled.html', {
                    'title': 'Page Temporarily Unavailable',
                }, status=503)

        return fn(request, *args, **kwargs)

    return _decorator
