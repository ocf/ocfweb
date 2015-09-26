from datetime import date
from datetime import datetime

from ocflib.lab.hours import DayHours

from ocfweb.component.banner import get_banner_message


def ocf_template_processor(request):
    now = datetime.now()
    today = date.today()
    hours = DayHours.from_date(today)

    banner = get_banner_message()

    return {
        'lab_is_open': hours.is_open(now),
        'current_lab_hours': hours,
        'force_lab_closed': banner.visible and banner.force_lab_closed,
    }
