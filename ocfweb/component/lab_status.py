from collections import namedtuple

import requests
import yaml

from ocfweb.caching import periodic


class LabStatus(namedtuple('LabStatus', [
    'force_lab_closed',
    'banner_html',
])):
    pass


@periodic(60)
def get_lab_status():
    """Get the front page banner message from the default location."""
    try:
        with open('/home/s/st/staff/lab_status.yaml') as f:
            tree = yaml.safe_load(f)
    except IOError:
        tree = yaml.safe_load(requests.get(
            'https://www.ocf.berkeley.edu/~staff/lab_status.yaml').text)
    return LabStatus(
        force_lab_closed=tree['force_lab_closed'],
        banner_html=tree['banner_html'] if tree['banner_visible'] else ''
    )
