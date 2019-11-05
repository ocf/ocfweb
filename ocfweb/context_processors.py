import re
from ipaddress import ip_address
from typing import Any
from typing import Dict
from typing import Generator

from django.http import HttpRequest
from django.urls import reverse
from ipware import get_client_ip
from ocflib.account.search import user_is_group
from ocflib.infra.net import is_ocf_ip

from ocfweb.api.hours import get_hours_listing
from ocfweb.component.lab_status import get_lab_status
from ocfweb.component.session import logged_in_user
from ocfweb.environment import ocfweb_version


def get_base_css_classes(request: HttpRequest) -> Generator[str, None, None]:
    if request.resolver_match and request.resolver_match.url_name:
        page_class = 'page-' + request.resolver_match.url_name
        yield page_class

        for arg in request.resolver_match.args:
            page_class += '-' + re.sub(r'[^a-zA-Z_\-]', '-', arg)
            yield page_class


def ocf_template_processor(request: HttpRequest) -> Dict[str, Any]:
    hours_listing = get_hours_listing()
    real_ip, _ = get_client_ip(request)
    user = logged_in_user(request)
    return {
        'base_css_classes': ' '.join(get_base_css_classes(request)),
        'current_lab_hours': hours_listing.hours_on_date(),
        'holidays': hours_listing.holidays,
        'is_ocf_ip': is_ocf_ip(ip_address(real_ip)) if real_ip else True,
        'join_staff_url': request.build_absolute_uri(reverse('about-staff')),
        'lab_is_open': hours_listing.is_open(),
        'lab_status': get_lab_status(),
        'ocfweb_version': ocfweb_version(),
        'request_full_path': request.get_full_path(),
        'user': user,
        'user_is_group': user is not None and user_is_group(user),
    }
