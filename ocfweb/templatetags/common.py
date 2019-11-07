import json as json_
from typing import Any
from typing import Iterable
from typing import MutableMapping

from django import template

register = template.Library()


@register.filter
def getitem(obj: MutableMapping[Any, Any], item: Any) -> Any:
    """Grab the item from the object.

    Example usage:
        someObj|getitem:key
    """
    return obj[item]


@register.filter
def sum_values(obj: Any) -> Any:
    """Return sum of the object's values."""
    return sum(obj.values())


@register.filter
def sort(items: Iterable[Any]) -> Iterable[Any]:
    """Sort items.

    Consider using the built-in `dictsort` filter if you're sorting
    dictionaries.

    I cannot understand why Django doesn't have this built-in (or allow you to
    call `sorted` yourself from inside a template).
    """
    return sorted(items)


@register.filter
def join(items: Iterable[Any], s: str) -> str:
    """Join items (probably of an array).

    Example usage:
        myArray|join:','
    """
    return s.join(items)


@register.filter
def json(obj: object) -> str:
    return json_.dumps(obj)
