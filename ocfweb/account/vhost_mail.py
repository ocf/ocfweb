import re
from contextlib import contextmanager

from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.http import require_POST
from ocflib.account.validators import validate_password
from ocflib.vhost.mail import crypt_password
from ocflib.vhost.mail import get_connection
from ocflib.vhost.mail import MailForwardingAddress
from ocflib.vhost.mail import vhosts_for_user

from ocfweb.auth import group_account_required
from ocfweb.auth import login_required
from ocfweb.component.errors import ResponseException
from ocfweb.component.session import logged_in_user


class REMOVE_PASSWORD:
    """Singleton to represent a password should be removed."""


@login_required
@group_account_required
def vhost_mail(request):
    user = logged_in_user(request)
    vhosts = []

    with _txn() as c:
        for vhost in sorted(vhosts_for_user(user)):
            addresses = sorted(vhost.get_forwarding_addresses(c))
            vhosts.append({
                'domain': vhost.domain,
                'addresses': addresses,
                'has_wildcard': any(address.is_wildcard for address in addresses),
            })

    return render(
        request,
        'account/vhost_mail/index.html',
        {
            'title': 'Mail Virtual Hosting',
            'vhosts': vhosts,
        },
    )


@login_required
@group_account_required
@require_POST
def vhost_mail_update(request):
    user = logged_in_user(request)

    # All requests are required to have these
    action = _get_action(request)
    addr_name, addr_domain, addr_vhost = _get_addr(request, user, 'addr', required=True)
    addr = (addr_name or '') + '@' + addr_domain

    # These fields are optional; some might be None
    forward_to = _get_forward_to(request)

    new_addr = _get_addr(request, user, 'new_addr', required=False)
    new_addr_name = None
    if new_addr is not None:
        new_addr_name, new_addr_domain, new_addr_vhost = new_addr
        new_addr = (new_addr_name or '') + '@' + new_addr_domain

        # Sanity check: can't move addresses across vhosts
        if new_addr_vhost != addr_vhost:
            _error(
                request,
                'You cannot change an address from "{}" to "{}"!'.format(
                    addr_domain, new_addr_domain,
                ),
            )

    password_hash = _get_password(request, new_addr_name or addr_name)

    # Perform the add/update
    with _txn() as c:
        existing = _find_addr(c, addr_vhost, addr)
        new = None

        if action == 'add':
            if existing is not None:
                _error(request, 'The address "{}" already exists!'.format(addr))

            new = MailForwardingAddress(
                address=addr,
                crypt_password=None,
                forward_to=None,
                last_updated=None,
            )
        else:
            if existing is None:
                _error(request, 'The address "{}" does not exist!'.format(addr))
            addr_vhost.remove_forwarding_address(c, existing.address)

        if action != 'delete':
            new = new or existing
            if forward_to:
                new = new._replace(forward_to=forward_to)
            if password_hash is REMOVE_PASSWORD:
                new = new._replace(crypt_password=None)
            elif password_hash:
                new = new._replace(crypt_password=password_hash)
            if new_addr:
                new = new._replace(address=new_addr)

        if new is not None:
            addr_vhost.add_forwarding_address(c, new)

    messages.add_message(request, messages.SUCCESS, 'Update successful!')
    return _redirect_back()


def _error(request, msg):
    messages.add_message(request, messages.ERROR, msg)
    raise ResponseException(_redirect_back())


def _redirect_back():
    return redirect(reverse('vhost_mail'))


def _get_action(request):
    action = request.POST.get('action')
    if action not in {'add', 'update', 'delete'}:
        _error(request, 'Invalid action: "{}"'.format(action))
    else:
        return action


def _parse_addr(addr, allow_wildcard=False):
    """Safely parse an email, returning first component and domain."""
    m = re.match(
        (
            r'([a-zA-Z0-9\-_\+\.]+)' +
            ('?' if allow_wildcard else '') +
            r'@([a-zA-Z0-9\-_\+\.]+)$'
        ),
        addr,
    )
    if not m:
        return None
    name, domain = m.group(1), m.group(2)
    if '.' in domain:
        return name, domain


def _get_addr(request, user, field, required=True):
    original = request.POST.get(field)
    if original is not None:
        addr = original.strip()
        parsed = _parse_addr(addr, allow_wildcard=True)
        if not parsed:
            _error(request, 'Invalid address: "{}"'.format(original))
        else:
            name, domain = parsed

            # Make sure that user can use this domain
            vhost = _get_vhost(user, domain)
            if vhost is not None:
                return name, domain, vhost
            else:
                _error(request, 'You cannot use the domain: "{}"'.format(domain))
    elif required:
        _error(request, 'You must provide an address!')


def _get_forward_to(request):
    forward_to = request.POST.get('forward_to')

    if forward_to is None:
        return None

    # Validate each email in the list
    parsed_addrs = set()
    for forward_addr in forward_to.split(','):
        # Strip whitespace and ignore empty, because people suck at forms.
        forward_addr = forward_addr.strip()
        if forward_addr != '':
            if _parse_addr(forward_addr) is not None:
                parsed_addrs.add(forward_addr)
            else:
                _error(request, 'Invalid forwarding address: "{}"'.format(forward_addr))

    if len(parsed_addrs) < 1:
        _error(request, 'You must provide at least one address to forward to!')

    return frozenset(parsed_addrs)


def _get_password(request, addr_name):
    # If addr_name is None, then this is a wildcard address, and those can't
    # have passwords.
    if addr_name is None:
        return REMOVE_PASSWORD

    password = request.POST.get('password')
    if password is not None:
        password = password.strip()
        if not password:
            return REMOVE_PASSWORD
        try:
            validate_password(addr_name, password, strength_check=True)
        except ValueError as ex:
            _error(request, ex.args[0])
        else:
            return crypt_password(password)


def _get_vhost(user, domain):
    vhosts = vhosts_for_user(user)
    for vhost in vhosts:
        if vhost.domain == domain:
            return vhost


def _find_addr(c, vhost, addr):
    for addr_obj in vhost.get_forwarding_addresses(c):
        if addr_obj.address == addr:
            return addr_obj


@contextmanager
def _txn(**kwargs):
    with get_connection(
        user=settings.OCFMAIL_USER,
        password=settings.OCFMAIL_PASSWORD,
        db=settings.OCFMAIL_DB,
        autocommit=False,
        **kwargs
    ) as c:
        try:
            yield c
        except:
            c.connection.rollback()
            raise
        else:
            c.connection.commit()
