from urllib.parse import urlencode
from uuid import uuid4

from django import template

register = template.Library()


# public api key
OCF_API_KEY = 'AIzaSyC4st-AHFMr1O-59eaoT2AGjvX_zHtbdN8'

OCF_LATITUDE = 37.869488
OCF_LONGITUDE = -122.257522

NEW_OCF_LATITUDE = 37.869179
NEW_OCF_LONGITUDE = -122.259364


@register.inclusion_tag('partials/google-map.html')
def google_map(width, height, show_info=True):
    return {
        'width': width,
        'height': height,
        'show_info': show_info,
        'id': uuid4(),
        'ocf_api_key': OCF_API_KEY,
        'ocf_latitude': OCF_LATITUDE,
        'ocf_longitude': OCF_LONGITUDE,
    }


# TODO: remove this duplicated code and template
@register.inclusion_tag('partials/new-google-map.html')
def new_google_map(width, height, show_info=True):
    return {
        'width': width,
        'height': height,
        'show_info': show_info,
        'id': uuid4(),
        'ocf_api_key': OCF_API_KEY,
        'ocf_latitude': NEW_OCF_LATITUDE,
        'ocf_longitude': NEW_OCF_LONGITUDE,
    }


@register.inclusion_tag('partials/google-map-static.html')
def google_map_static(width, height):
    return {
        'url': 'https://maps.googleapis.com/maps/api/staticmap?{}'.format(
            urlencode({
                'size': '{}x{}'.format(width, height),
                'zoom': 17,
                'center': '{},{}'.format(OCF_LATITUDE, OCF_LONGITUDE),
                'markers': 'label:OCF|size:mid|{},{}'.format(OCF_LATITUDE, OCF_LONGITUDE),

                'key': OCF_API_KEY,
            })
        ),
    }
