from collections import namedtuple

from django import template
from django.core.urlresolvers import reverse

register = template.Library()

_NavItem = namedtuple('NavItem', ['url', 'title', 'active'])


@register.inclusion_tag('partials/stats-navbar.html', takes_context=True)
def stats_navbar(context):
    return {
        'navbar': [
            _NavItem(
                url=reverse(name),
                title=title,
                active=context['request'].resolver_match.url_name == name,
            )
            for name, title in
            [
                ('stats', 'Summary'),
                ('stats_printing', 'Printing'),
                ('stats_accounts', 'Accounts'),
            ]
        ],
    }
