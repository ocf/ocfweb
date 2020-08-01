from typing import Any
from typing import Dict
from urllib.parse import urlencode
from uuid import uuid4

from django import template

register = template.Library()


# public api key
OCF_API_KEY = 'AIzaSyC4st-AHFMr1O-59eaoT2AGjvX_zHtbdN8'

OCF_LATITUDE = 37.869724
OCF_LONGITUDE = -122.259715


@register.inclusion_tag('partials/google-map.html')
def google_map(width: float, height: float, show_info: bool = True) -> Dict[str, Any]:
    return {
        'width': width,
        'height': height,
        'show_info': show_info,
        'id': uuid4(),
        'ocf_api_key': OCF_API_KEY,
        'ocf_latitude': OCF_LATITUDE,
        'ocf_longitude': OCF_LONGITUDE,
    }


@register.inclusion_tag('partials/google-map-static.html')
def google_map_static(width: float, height: float, display_width: str) -> Dict[str, Any]:
    return {
        'url': 'https://maps.googleapis.com/maps/api/staticmap?{}'.format(
            urlencode({
                'size': f'{width}x{height}',
                'zoom': 17,
                'center': f'{OCF_LATITUDE},{OCF_LONGITUDE}',
                'markers': f'size:mid|{OCF_LATITUDE},{OCF_LONGITUDE}',
                'scale': 2,
                'key': OCF_API_KEY,
            }),
        ),
        'display_width': display_width,
    }
