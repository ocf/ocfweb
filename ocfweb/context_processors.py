from datetime import date
from datetime import datetime

from ocflib.lab.hours import DayHours

from ocfweb.component.lab_status import get_lab_status


def ocf_template_processor(request):
    now = datetime.now()
    today = date.today()
    hours = DayHours.from_date(today)

    return {
        'lab_is_open': hours.is_open(now),
        'current_lab_hours': hours,
        'lab_status': get_lab_status(),
    }
