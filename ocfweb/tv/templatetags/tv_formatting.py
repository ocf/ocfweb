from django import template

register = template.Library()


@register.filter
def tv_lab_hours(hour):
    if hour:
        if hour.open.minute != 0 or hour.close.minute != 0:
            fmt = '{:%-I:%M%P}–{:%-I%M%P}'
        else:
            fmt = '{:%-I%P}–{:%-I%P}'

        return fmt.format(hour.open, hour.close)
