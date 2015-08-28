from django import template

register = template.Library()


@register.filter
def lab_hours_day_and_holiday(hours):
    if hours.holiday:
        return '{hours.name} ({hours.holiday})'.format(hours=hours)
    return hours.name


@register.filter
def lab_hours_time(hours):
    if None not in [hours.open, hours.close]:
        def format_hour(hour):
            """Format an hour with am / pm."""
            if hour == 0:
                return '12am'
            elif hour <= 12:
                return str(hour) + 'am'
            else:
                return str(hour % 12) + 'pm'

        return '{}–{}'.format(format_hour(hours.open), format_hour(hours.close))
    else:
        return 'Closed All Day'
