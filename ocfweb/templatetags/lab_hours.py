from django import template

register = template.Library()


@register.filter
def lab_hours_holiday(hours):
    if hours.holiday:
        return '({})'.format(hours.holiday)
    return ''


@register.filter
def lab_hours_time(hours):
    if hours:
        return ',\xa0\xa0'.join(  # two non-breaking spaces
            '{:%-I:%M%P}–{:%-I:%M%P}'.format(hour.open, hour.close)
            if hour.open.minute != 0 or hour.close.minute != 0
            else '{:%-I%P}–{:%-I%P}'.format(hour.open, hour.close)
            for hour in hours
        )
    else:
        return 'Closed All Day'
