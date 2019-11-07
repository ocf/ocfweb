from typing import Any

from django import template

register = template.Library()


@register.filter
def gravatar(staffer: Any, size: int) -> str:
    return staffer.gravatar(size)
