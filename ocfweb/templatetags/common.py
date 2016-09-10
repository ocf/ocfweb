import json

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
def sort(items):
    """Sort items.

    Consider using the built-in `dictsort` filter if you're sorting
    dictionaries.

    I cannot understand why Django doesn't have this built-in (or allow you to
    call `sorted` yourself from inside a template).
    """
    return sorted(items)


@register.filter('json')
def json_(obj):
    """Output JSON.

    Be warned that this can safely be used in HTML (as long as you use regular
    escaping and don't mark it as safe), but *cannot* be used safely in
    <script> tags in any context.

    https://code.djangoproject.com/ticket/17419
    """
    return json.dumps(obj)
