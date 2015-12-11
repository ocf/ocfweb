from django import template

register = template.Library()


@register.inclusion_tag('partials/progress-bar.html')
def progress_bar(label, value, max):
    """Render a Bootstrap progress bar.

    :param label:
    :param value:
    :param max:

    Example usage:
        {% progress_bar label='Toner: 448 pages remaining' value=448 max=24000 %}
    """

    print(value)

    return {
        'label': label,
        'percent': int((value / max) * 100),
        'value': value,
        'max': max,
    }
