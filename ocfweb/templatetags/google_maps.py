from uuid import uuid4

from django import template

register = template.Library()


@register.inclusion_tag('partials/google-map.html')
def google_map(width, height):
    return {
        'width': width,
        'height': height,
        'id': uuid4(),
    }
