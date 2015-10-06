import re
from datetime import date
from datetime import datetime
from ipaddress import ip_address
from ipaddress import ip_network

from ipware.ip import get_real_ip
from ocflib.lab.hours import DayHours

from ocfweb.component.lab_status import get_lab_status


def is_ocf_ip(ip):
    # TODO: move this to ocflib when it drops Python 3.2 support
    return ip_address(ip) in ip_network('169.229.10.0/24')


def ocf_template_processor(request):
    now = datetime.now()
    today = date.today()
    hours = DayHours.from_date(today)

    base_css_classes = []
    if request.resolver_match.url_name:
        page_class = 'page-' + request.resolver_match.url_name
        base_css_classes.append(page_class)

        for arg in request.resolver_match.args:
            page_class += '-' + re.sub('[^a-zA-Z_\-]', '-', arg)
            base_css_classes.append(page_class)

    real_ip = get_real_ip(request)

    return {
        'lab_is_open': hours.is_open(now),
        'current_lab_hours': hours,
        'lab_status': get_lab_status(),
        'base_css_classes': ' '.join(base_css_classes),
        'is_ocf_ip': is_ocf_ip(real_ip) if real_ip else True,
    }
