import json as json_

from django import template

register = template.Library()


@register.filter
def getitem(obj, item):
    """Grab the item from the object.

    Example usage:
        someObj|getitem:key
    """
    return obj[item]


@register.filter
def sum_values(obj):
    """Return sum of the object's values."""
    return sum(obj.values())


@register.filter
def sort(items):
    """Sort items.

    Consider using the built-in `dictsort` filter if you're sorting
    dictionaries.

    I cannot understand why Django doesn't have this built-in (or allow you to
    call `sorted` yourself from inside a template).
    """
    return sorted(items)


@register.filter
def join(items, s):
    """Join items (probably of an array).

    Example usage:
        myArray|join:','
    """
    return s.join(items)


@register.filter
def json(obj):
    return json_.dumps(obj)
