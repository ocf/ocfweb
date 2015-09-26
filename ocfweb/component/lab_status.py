from collections import namedtuple

import requests
import yaml


class LabStatus(namedtuple('LabStatus', [
    'force_lab_closed',
    'banner_html',
])):
    pass


def get_lab_status():
    """Get the front page banner message from the default location."""
    try:
        with open('/home/s/st/staff/lab_status.yaml') as f:
            tree = yaml.safe_load(f)
    except IOError:
        return requests.get(
            'https://www.ocf.berkeley.edu/~staff/lab_status.yaml').text
    return LabStatus(
        force_lab_closed=tree['force_lab_closed'],
        banner_html=tree['banner_html'] if tree['banner_visible'] else ''
    )
