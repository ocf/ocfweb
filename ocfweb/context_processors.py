from datetime import date
from datetime import datetime

from ocflib.lab.hours import DayHours


def ocf_template_processor(request):
    now = datetime.now()
    today = date.today()
    hours = DayHours.from_date(today)

    if None not in [hours.open, hours.close]:
        lab_hours_text = 'asdf'
    else:
        lab_hours_text = 'Closed All Day'
    lab_hours_text += ' — {}'.format(hours.name)

    return {
        'lab_is_open': hours.is_open(now),
        'lab_hours_text': lab_hours_text,
    }
