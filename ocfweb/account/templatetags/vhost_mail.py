from django import template

register = template.Library()


@register.filter
def forwarding_addresses(vhost, c):
    return vhost.get_forwarding_addresses(c)


@register.filter
def address_to_parts(address):
    return address.split('@')
