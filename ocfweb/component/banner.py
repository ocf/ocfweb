from collections import namedtuple
from urllib.request import urlopen

import yaml


class BannerMessage(namedtuple('BannerMessage', [
    'visible',
    'force_lab_closed',
    'html',
])):
    pass


def get_banner_message():
    """Get the front page banner message from the default location."""
    with urlopen('file:///home/s/st/staff/banner.yaml') as f:
        tree = yaml.load(f)
    return BannerMessage(
        visible=tree['visible'],
        force_lab_closed=tree['force_lab_closed'],
        html=tree['html'],
    )
