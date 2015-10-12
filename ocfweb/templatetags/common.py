from django import template

register = template.Library()


@register.filter
def getitem(obj, item):
    """Grab the item from the object.

    Example usage:
        someObj|getitem:key
    """
    return obj[item]
