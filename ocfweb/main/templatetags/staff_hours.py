from django import template

register = template.Library()


@register.filter
def gravatar(staffer, size):
    return staffer.gravatar(size)
