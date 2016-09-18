from django import template

register = template.Library()


@register.filter
def address_to_parts(address):
    return address.split('@')
