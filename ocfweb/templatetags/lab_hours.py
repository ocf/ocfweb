from django import template

register = template.Library()


@register.filter
def lab_hours_day_and_holiday(hours):
    if hours.holiday:
        return '{hours.weekday} ({hours.holiday})'.format(hours=hours)
    return hours.weekday


@register.filter
def lab_hours_time(day):
    if day.hours:
        def format_hour(hour):
            """Format an hour with am / pm."""
            if hour == 0:
                return '12am'
            elif hour < 12:
                return str(hour) + 'am'
            elif hour == 12:
                return '12pm'
            else:
                return str(hour % 12) + 'pm'

        return ',\xa0\xa0'.join(  # two non-breaking spaces
            '{}–{}'.format(format_hour(hours.open), format_hour(hours.close))
            for hours in day.hours
        )
    else:
        return 'Closed All Day'
