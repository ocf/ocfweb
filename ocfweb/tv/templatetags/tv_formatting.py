from django import template

register = template.Library()


@register.filter
def tv_lab_hours(hour):
    if hour:
        if hour.open.minute != 0 or hour.close.minute != 0:
            fmt = '{:%-I:%M%P}–{:%-I:%M%P}'
        else:
            fmt = '{:%-I%P}–{:%-I%P}'

        return fmt.format(hour.open, hour.close)


@register.filter
def tv_lab_hours_css(hours):
    # 9:30 = hours-small, 9:00 = hours-large
    return 'hours-small' if any(edge.minute != 0
                                for block in hours
                                for edge in block) else 'hours-large'
