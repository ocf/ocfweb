from socket import getaddrinfo, gaierror
from django.conf import settings
from django.core.exceptions import ValidationError


def _email_host(email_addr):
    """Returns the host in the email address argument"""
    if "@" in email_addr:
        return email_addr.rsplit("@", 1).pop()
    return None


def _host_exists(host):
    try:
        host_info = getaddrinfo(host, None)
    except gaierror:
        return False
    else:
        return host_info


def validate_email_host_exists(email_addr):
    """Verifies that the host of the email address exists"""
    host = _email_host(email_addr)
    if not _host_exists(host):
        raise ValidationError("E-mail address host does not exist.")


def validate_username_not_reserved(username):
    """Verifies that the username requested is not in the list of reserved names"""
    username_lower = username.lower()
    with open(settings.OCF_RESERVED_NAMES_LIST, "r") as f:
        for reserved_name in f:
            reserved_name = reserved_name.strip().lower()
            if username_lower == reserved_name:
                raise ValidationError("Requested account name is a reserved system name.")
