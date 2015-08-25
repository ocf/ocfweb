from collections import OrderedDict
from datetime import date
from datetime import datetime

from ocflib.lab.hours import DayHours


def ocf_template_processor(request):
    now = datetime.now()
    today = date.today()
    hours = DayHours.from_date(today)

    return {
        'lab_is_open': hours.is_open(now),
        'current_lab_hours': hours,
        'ocf_status': OrderedDict([
            ('Web', True),  # if you can see this page, web is up :)

            # TODO: real statuses
            ('Printing', True),
            ('Email', True),
            ('SSH', False),
        ]),
    }
