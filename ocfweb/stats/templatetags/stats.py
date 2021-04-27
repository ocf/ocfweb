from collections import namedtuple
from typing import Any
from typing import Dict
from typing import Mapping

from django import template
from django.urls import reverse

register = template.Library()

_NavItem = namedtuple('_NavItem', ['url', 'title', 'active'])


@register.inclusion_tag('stats/partials/stats-navbar.html', takes_context=True)
def stats_navbar(context: Mapping[Any, Any]) -> Dict[str, Any]:
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
                # TODO: probably a better place to put this
                ('pages_printed', 'Lifetime Pages Printed'),
                ('stats_accounts', 'Accounts'),
                ('stats_mirrors', 'Mirrors'),
                ('session-stats', 'Session Statistics'),
            ]
        ],
    }
