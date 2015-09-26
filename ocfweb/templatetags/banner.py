from django import template

register = template.Library()


@register.filter
def lab_hours_day_and_holiday(hours):
    if hours.holiday:
        return '{hours.weekday} ({hours.holiday})'.format(hours=hours)
    return hours.weekday
