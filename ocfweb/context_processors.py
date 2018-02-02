import re
from datetime import date
from ipaddress import ip_address

from django.urls import reverse
from ipware.ip import get_real_ip
from ocflib.account.search import user_is_group
from ocflib.infra.net import is_ocf_ip
from ocflib.lab.hours import Day

from ocfweb.component.lab_status import get_lab_status
from ocfweb.component.session import logged_in_user
from ocfweb.environment import ocfweb_version


def get_base_css_classes(request):
    if request.resolver_match.url_name:
        page_class = 'page-' + request.resolver_match.url_name
        yield page_class

        for arg in request.resolver_match.args:
            page_class += '-' + re.sub(r'[^a-zA-Z_\-]', '-', arg)
            yield page_class


def ocf_template_processor(request):
    hours = Day.from_date(date.today())
    real_ip = get_real_ip(request)
    user = logged_in_user(request)
    return {
        'base_css_classes': ' '.join(get_base_css_classes(request)),
        'current_lab_hours': hours,
        'is_ocf_ip': is_ocf_ip(ip_address(real_ip)) if real_ip else True,
        'join_staff_url': request.build_absolute_uri(reverse('about-staff')),
        'lab_is_open': hours.is_open(),
        'lab_status': get_lab_status(),
        'ocfweb_version': ocfweb_version(),
        'request_full_path': request.get_full_path(),
        'user': user,
        'user_is_group': user is not None and user_is_group(user),
    }
