import operator

from django import template

register = template.Library()


@register.filter
def forwarding_addresses(vhost, c):
    return sorted(
        vhost.get_forwarding_addresses(c),
        key=operator.attrgetter('address'),
    )


@register.filter
def address_to_parts(address):
    return address.split('@')
