from collections import OrderedDict
from datetime import date
from datetime import datetime

from ocflib.lab.hours import DayHours


def ocf_template_processor(request):
    now = datetime.now()
    today = date.today()
    hours = DayHours.from_date(today)

    if None not in [hours.open, hours.close]:
        def format_hour(hour):
            """Format an hour with am / pm."""
            if hour == 0:
                return '12am'
            elif hour <= 12:
                return str(hour) + 'am'
            else:
                return str(hour % 12) + 'pm'

        lab_hours_text = '{}—{}'.format(format_hour(hours.open), format_hour(hours.close))
    else:
        lab_hours_text = ''
    lab_hours_text += ' ' + hours.name

    return {
        'lab_is_open': hours.is_open(now),
        'lab_hours_text': lab_hours_text,
        'ocf_status': OrderedDict([
            ('Web', True),  # if you can see this page, web is up :)

            # TODO: real statuses
            ('Printing', True),
            ('Email', True),
            ('SSH', False),
        ]),
    }
