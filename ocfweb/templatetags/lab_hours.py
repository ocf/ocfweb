from datetime import date
from typing import Any
from typing import Iterable
from typing import Optional

from django import template

register = template.Library()


@register.simple_tag
def lab_hours_holiday(holidays: Iterable[Any], when: Optional[date] = None) -> str:
    if when is None:
        when = date.today()

    for holiday in holidays:
        if holiday.startdate <= when <= holiday.enddate:
            return f'({holiday.reason})'
    return ''


@register.filter
def lab_hours_time(hours: Optional[Iterable[Any]]) -> str:
    if hours:
        return ',\xa0\xa0'.join(  # two non-breaking spaces
            f'{hour.open:%-I:%M%P}–{hour.close:%-I:%M%P}'
            if hour.open.minute != 0 or hour.close.minute != 0
            else f'{hour.open:%-I%P}–{hour.close:%-I%P}'
            for hour in hours
        )
    else:
        return 'Closed All Day'
