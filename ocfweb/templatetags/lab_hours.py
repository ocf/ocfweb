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
            '{:%-I%P}–{:%-I%P}'.format(hours.open, hours.close)
            for hours in hours
        )
    else:
        return 'Closed All Day'
