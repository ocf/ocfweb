from collections import namedtuple

import yaml

from ocfweb.caching import periodic


LabStatus = namedtuple(
    'LabStatus', [
        'force_lab_closed',
        'banner_html',
    ],
)


@periodic(60, ttl=86400)
def get_lab_status():
    """Get the front page banner message from the default location."""
    with open('/etc/ocf/lab_status.yaml') as f:
        tree = yaml.safe_load(f)
    return LabStatus(
        force_lab_closed=tree['force_lab_closed'],
        banner_html=tree['banner_html'] if tree['banner_visible'] else '',
    )
