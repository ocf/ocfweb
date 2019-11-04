from typing import List

from django import template

register = template.Library()


@register.filter
def address_to_parts(address: str) -> List[str]:
    return address.split('@')
