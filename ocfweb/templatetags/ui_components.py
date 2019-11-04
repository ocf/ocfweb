from typing import Any
from typing import Dict

from django import template
register = template.Library()


@register.inclusion_tag('partials/progress-bar.html')
def progress_bar(label: str, value: int, max: int) -> Dict[str, Any]:
    """Render a Bootstrap progress bar.

    :param label:
    :param value:
    :param max:

    Example usage:
        {% progress_bar label='Toner: 448 pages remaining' value=448 max=24000 %}
    """
    return {
        'label': label,
        'percent': int((value / max) * 100),
        'value': value,
        'max': max,
    }
