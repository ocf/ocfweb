from django import template

from ocfweb.templatetags.lab_hours import lab_hours_holiday as holiday_hours

register = template.Library()


@register.filter
def gravatar(staffer, size):
    return staffer.gravatar(size)

@register.filter
def lab_holidays(hours):
    return holiday_hours(hours)


