from contextlib import contextmanager
from datetime import datetime

import mock
import pytest
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from ocflib.vhost.mail import MailForwardingAddress

from ocfweb.account import vhost_mail
from ocfweb.account.vhost_mail import _error
from ocfweb.account.vhost_mail import _find_addr
from ocfweb.account.vhost_mail import _get_action
from ocfweb.account.vhost_mail import _get_addr
from ocfweb.account.vhost_mail import _get_forward_to
from ocfweb.account.vhost_mail import _get_password
from ocfweb.account.vhost_mail import _get_vhost
from ocfweb.account.vhost_mail import _parse_addr
from ocfweb.account.vhost_mail import _redirect_back
from ocfweb.account.vhost_mail import _txn
from ocfweb.component.errors import ResponseException


ALL_VIEWS = ('vhost_mail', 'vhost_mail_update')


@pytest.mark.parametrize('view', ALL_VIEWS)
def test_view_requires_login(view, client):
    """Logged out users should get redirected to login."""
    resp = client.get(reverse(view))
    assert resp.status_code == 302
    assert resp.url == reverse('login')


@pytest.mark.parametrize('view', ALL_VIEWS)
def test_view_requires_group_account(view, client_guser):
    """Individual accounts should get an error."""
    resp = client_guser.get(reverse(view))
    assert resp.status_code == 403


def test_main_view_works(client_ggroup):
    """Smoke test with a valid user."""
    with mock.patch.object(vhost_mail, 'vhosts_for_user', return_value=[]):
        resp = client_ggroup.get(reverse('vhost_mail'))
        assert resp.status_code == 200


@pytest.yield_fixture
def mock_ggroup_vhost():
    mocked_vhost = mock.Mock(user='ggroup', domain='vhost.com')
    mocked_vhost2 = mock.Mock(user='ggroup', domain='vhost2.com')
    mocked_vhost.get_forwarding_addresses.return_value = {
        MailForwardingAddress(
            address='exists@vhost.com',
            crypt_password='crypt',
            forward_to=frozenset(('bob@gmail.com', 'tom@gmail.com')),
            last_updated=datetime(2000, 1, 1),
        ),
    }
    with mock.patch.object(vhost_mail, 'vhosts_for_user', return_value={
        mocked_vhost, mocked_vhost2,
    }):
        yield mocked_vhost


@pytest.yield_fixture
def mock_txn():
    with mock.patch.object(vhost_mail, '_txn') as m:
        yield m


@pytest.yield_fixture
def mock_messages():
    with mock.patch.object(vhost_mail.messages, 'add_message') as m:
        yield m


def test_update_add_new_addr(client_ggroup, mock_ggroup_vhost, mock_messages, mock_txn):
    resp = client_ggroup.post(reverse('vhost_mail_update'), {
        'action': 'add',
        'addr': 'john@vhost.com',
        'forward_to': 'john@gmail.com,bob@gmail.com',
        'password': 'nice password bro',
    })
    mock_ggroup_vhost.add_forwarding_address.assert_called_once_with(
        mock_txn().__enter__(),
        MailForwardingAddress(
            address='john@vhost.com',
            forward_to=frozenset(('john@gmail.com', 'bob@gmail.com')),
            crypt_password=mock.ANY,
            last_updated=None,
        ),
    )
    assert resp.status_code == 302
    mock_messages.assert_called_once_with(
        mock.ANY,
        messages.SUCCESS,
        'Update successful!',
    )


def test_update_add_new_addr_already_exists(client_ggroup, mock_ggroup_vhost, mock_messages, mock_txn):
    resp = client_ggroup.post(reverse('vhost_mail_update'), {
        'action': 'add',
        'addr': 'exists@vhost.com',
        'forward_to': 'john@gmail.com,bob@gmail.com',
        'password': 'nice password bro',
    })
    assert not mock_ggroup_vhost.add_forwarding_address.called
    assert resp.status_code == 302
    mock_messages.assert_called_once_with(
        mock.ANY,
        messages.ERROR,
        'The address "exists@vhost.com" already exists!',
    )


def test_update_fails_to_add_addr_to_bad_vhost(client_ggroup, mock_ggroup_vhost, mock_messages, mock_txn):
    resp = client_ggroup.post(reverse('vhost_mail_update'), {
        'action': 'add',
        'addr': 'john@bad-vhost.com',
        'forward_to': 'john@gmail.com,bob@gmail.com',
        'password': 'nice password bro',
    })
    mock_ggroup_vhost.add_forwarding_address.called
    assert resp.status_code == 302
    mock_messages.assert_called_once_with(
        mock.ANY,
        messages.ERROR,
        'You cannot use the domain: "bad-vhost.com"',
    )


def test_update_delete_addr(client_ggroup, mock_ggroup_vhost, mock_messages, mock_txn):
    resp = client_ggroup.post(reverse('vhost_mail_update'), {
        'action': 'delete',
        'addr': 'exists@vhost.com',
    })
    assert not mock_ggroup_vhost.add_forwarding_address.called
    mock_ggroup_vhost.remove_forwarding_address.assert_called_once_with(
        mock_txn().__enter__(),
        'exists@vhost.com',
    )
    assert resp.status_code == 302
    mock_messages.assert_called_once_with(
        mock.ANY,
        messages.SUCCESS,
        'Update successful!',
    )


def test_update_delete_addr_nonexistent(client_ggroup, mock_ggroup_vhost, mock_messages, mock_txn):
    resp = client_ggroup.post(reverse('vhost_mail_update'), {
        'action': 'delete',
        'addr': 'john@vhost.com',
    })
    assert not mock_ggroup_vhost.add_forwarding_address.called
    assert not mock_ggroup_vhost.remove_forwarding_address.called
    assert resp.status_code == 302
    mock_messages.assert_called_once_with(
        mock.ANY,
        messages.ERROR,
        'The address "john@vhost.com" does not exist!',
    )


def test_update_replace_some_stuff(client_ggroup, mock_ggroup_vhost, mock_messages, mock_txn):
    resp = client_ggroup.post(reverse('vhost_mail_update'), {
        'action': 'update',
        'addr': 'exists@vhost.com',
        'new_addr': 'john@vhost.com',
        'forward_to': 'john@gmail.com,bob@gmail.com',
        'password': 'nice password bro',
    })
    mock_ggroup_vhost.remove_forwarding_address.assert_called_once_with(
        mock_txn().__enter__(),
        'exists@vhost.com',
    )
    mock_ggroup_vhost.add_forwarding_address.assert_called_once_with(
        mock_txn().__enter__(),
        MailForwardingAddress(
            address='john@vhost.com',
            forward_to=frozenset(('john@gmail.com', 'bob@gmail.com')),
            crypt_password=mock.ANY,
            last_updated=mock.ANY,
        ),
    )
    assert resp.status_code == 302
    mock_messages.assert_called_once_with(
        mock.ANY,
        messages.SUCCESS,
        'Update successful!',
    )


def test_update_replace_noop(client_ggroup, mock_ggroup_vhost, mock_messages, mock_txn):
    resp = client_ggroup.post(reverse('vhost_mail_update'), {
        'action': 'update',
        'addr': 'exists@vhost.com',
    })
    mock_ggroup_vhost.remove_forwarding_address.assert_called_once_with(
        mock_txn().__enter__(),
        'exists@vhost.com',
    )
    mock_ggroup_vhost.add_forwarding_address.assert_called_once_with(
        mock_txn().__enter__(),
        MailForwardingAddress(
            address='exists@vhost.com',
            forward_to=frozenset(('bob@gmail.com', 'tom@gmail.com')),
            crypt_password=mock.ANY,
            last_updated=mock.ANY,
        ),
    )
    assert resp.status_code == 302
    mock_messages.assert_called_once_with(
        mock.ANY,
        messages.SUCCESS,
        'Update successful!',
    )


def test_update_replace_addr_nonexistent(client_ggroup, mock_ggroup_vhost, mock_messages, mock_txn):
    resp = client_ggroup.post(reverse('vhost_mail_update'), {
        'action': 'update',
        'addr': 'john@vhost.com',
        'password': 'some great password',
    })
    assert not mock_ggroup_vhost.add_forwarding_address.called
    assert not mock_ggroup_vhost.remove_forwarding_address.called
    assert resp.status_code == 302
    mock_messages.assert_called_once_with(
        mock.ANY,
        messages.ERROR,
        'The address "john@vhost.com" does not exist!',
    )


def test_update_cant_move_addr_across_vhosts(client_ggroup, mock_ggroup_vhost, mock_messages, mock_txn):
    resp = client_ggroup.post(reverse('vhost_mail_update'), {
        'action': 'update',
        'addr': 'john@vhost.com',
        'new_addr': 'john@vhost2.com',
    })
    assert not mock_ggroup_vhost.add_forwarding_address.called
    assert not mock_ggroup_vhost.remove_forwarding_address.called
    assert resp.status_code == 302
    mock_messages.assert_called_once_with(
        mock.ANY,
        messages.ERROR,
        'You cannot change an address from "vhost.com" to "vhost2.com"!',
    )


def fake_request(**post_params):
    return mock.Mock(**{'POST.get': post_params.get})


def assert_resp_is_redirect(resp):
    assert isinstance(resp, HttpResponseRedirect)
    assert resp.status_code == 302
    assert resp.url == '/account/vhost/mail/'


def test_error():
    request = fake_request()
    with mock.patch.object(vhost_mail.messages, 'add_message') as fake_add_message, \
            pytest.raises(ResponseException) as ex:
        _error(request, 'asdf')

    assert_resp_is_redirect(ex.value.args[0])
    fake_add_message.assert_called_once_with(
        request, messages.ERROR, 'asdf',
    )


def test_redirect_back():
    assert_resp_is_redirect(_redirect_back())


@pytest.yield_fixture
def fake_error():
    class FakeError(Exception):
        pass

    def _fake_error(request, msg):
        raise FakeError(msg)

    with mock.patch.object(vhost_mail, '_error', side_effect=_fake_error):
        yield FakeError


@pytest.mark.parametrize('action', ('add', 'update', 'delete'))
def test_get_action_valid(action):
    assert _get_action(fake_request(action=action)) == action


@pytest.mark.parametrize('action', (None, '', 'replace', 'new', ' ', 'add '))
def test_get_action_invalid(action, fake_error):
    with pytest.raises(fake_error) as ex:
        _get_action(fake_request(action=action))
    assert ex.value.args[0] == 'Invalid action: "{}"'.format(action)


@pytest.mark.parametrize(('addr', 'expected'), [
    ('ckuehl@ocf.berkeley.edu', ('ckuehl', 'ocf.berkeley.edu')),
    ('ckuehl+yolo1._2+3@ocf.berkeley.edu', ('ckuehl+yolo1._2+3', 'ocf.berkeley.edu')),
    ('a@a.a', ('a', 'a.a')),
])
def test_parse_addr_success(addr, expected):
    assert _parse_addr(addr) == expected


@pytest.mark.parametrize('addr', [
    'ckuehl',
    '',
    '   ',
    '\t',
    ' ckuehl@ocf.berkeley.edu',
    'ckuehl\t@ocf.berkeley.edu',
    'ckuehl@',
    '@',
    '@ocf.berkeley.edu',
    'asdf@asdf',
])
def test_parse_addr_invalid(addr):
    assert _parse_addr(addr) is None


@pytest.mark.parametrize(('addr', 'name', 'domain'), (
    ('ckuehl@ocf.berkeley.edu', 'ckuehl', 'ocf.berkeley.edu'),
    ('john.doe+test@gmail.com', 'john.doe+test', 'gmail.com'),
))
@pytest.mark.parametrize('required', (False, True))
def test_get_addr_valid(addr, name, domain, required):
    fake_vhost = mock.Mock()
    with mock.patch.object(vhost_mail, '_get_vhost', return_value=fake_vhost):
        assert _get_addr(
            fake_request(addr=addr),
            'ggroup',
            'addr',
            required=required,
        ) == (name, domain, fake_vhost)


def test_get_addr_not_provided(fake_error):
    # with default: required
    with pytest.raises(fake_error) as ex:
        _get_addr(
            fake_request(),
            'ggroup',
            'addr',
        )
    assert ex.value.args[0] == 'You must provide an address!'

    # with required=False
    assert _get_addr(
        fake_request(),
        'ggroup',
        'addr',
        required=False,
    ) is None


@pytest.mark.parametrize('addr', ('', 'herp@', 'asdfg', 'a.b ', 'john.gmail.com'))
@pytest.mark.parametrize('required', (False, True))
def test_get_addr_invalid_addr(addr, required, fake_error):
    # with default: required
    with pytest.raises(fake_error) as ex:
        _get_addr(
            fake_request(addr=addr),
            'ggroup',
            'addr',
            required=required,
        )
    assert ex.value.args[0] == 'Invalid address: "{}"'.format(addr)


@pytest.mark.parametrize(('addr', 'domain'), (
    ('ckuehl@ocf.berkeley.edu', 'ocf.berkeley.edu'),
    ('john.doe+test@gmail.com', 'gmail.com'),
))
@pytest.mark.parametrize('required', (False, True))
def test_get_addr_no_permission(addr, domain, required, fake_error):
    with pytest.raises(fake_error) as ex, \
            mock.patch.object(vhost_mail, '_get_vhost', return_value=None):
        _get_addr(
            fake_request(addr=addr),
            'ggroup',
            'addr',
            required=required,
        )
    assert ex.value.args[0] == 'You cannot use the domain: "{}"'.format(domain)


@pytest.mark.parametrize(('forward_to', 'expected'), (
    (
        None,
        None,
    ),
    (
        'a@gmail.com',
        {'a@gmail.com'},
    ),
    (
        'a@gmail.com,b@gmail.com',
        {'a@gmail.com', 'b@gmail.com'},
    ),
    (
        'a@gmail.com , , b@gmail.com,, \n',
        {'a@gmail.com', 'b@gmail.com'},
    ),
))
def test_get_forward_to_valid(forward_to, expected):
    result = _get_forward_to(fake_request(forward_to=forward_to))
    assert result == expected


@pytest.mark.parametrize('forward_to', ('', ',    , , , ', '\n', '    '))
def test_get_forward_to_no_addrs_provided(forward_to, fake_error):
    with pytest.raises(fake_error) as ex:
        _get_forward_to(fake_request(forward_to=forward_to))
    assert ex.value.args[0] == 'You must provide at least one address to forward to!'


@pytest.mark.parametrize(('forward_to', 'first_invalid'), (
    ('a@a,b@gmail.com', 'a@a'),
    ('a@a,b', 'a@a'),
    ('asdf@gmail.com, ,   ,john.doe,boo@gmail.com', 'john.doe'),
))
def test_get_forward_to_invalid_addrs_provided(forward_to, first_invalid, fake_error):
    with pytest.raises(fake_error) as ex:
        _get_forward_to(fake_request(forward_to=forward_to))
    assert ex.value.args[0] == 'Invalid forwarding address: "{}"'.format(first_invalid)


def test_get_password_valid(fake_error):
    with mock.patch.object(vhost_mail, 'validate_password') as m, \
            mock.patch.object(vhost_mail, 'crypt_password') as c:
        assert _get_password(fake_request(password='password'), 'ckuehl') == c.return_value

    m.assert_called_once_with('ckuehl', 'password', strength_check=True)
    c.assert_called_once_with('password')


def test_get_password_fails_strength_check(fake_error):
    def fake_validate(addr_name, password, strength_check=False):
        raise ValueError('bad password yo')

    with pytest.raises(fake_error) as ex, \
            mock.patch.object(vhost_mail, 'validate_password', side_effect=fake_validate) as m:
        assert _get_password(fake_request(password='password'), 'ckuehl') is None

    assert ex.value.args[0] == 'bad password yo'
    m.assert_called_once_with('ckuehl', 'password', strength_check=True)


def test_get_password_empty():
    assert _get_password(fake_request(), 'ckuehl') is None


@pytest.yield_fixture
def fake_vhosts_for_user():
    vhosts = [
        mock.Mock(domain='google.com'),
        mock.Mock(domain='ocf.berkeley.edu'),
    ]
    with mock.patch.object(vhost_mail, 'vhosts_for_user', return_value=vhosts) as m:
        yield
    m.assert_called_once_with('ckuehl')


@pytest.mark.parametrize('domain', ('google.com', 'ocf.berkeley.edu'))
@pytest.mark.usefixtures('fake_vhosts_for_user')
def test_get_vhost_success(domain):
    assert _get_vhost('ckuehl', domain).domain == domain


@pytest.mark.parametrize('domain', ('gmail.com', 'berkeley.edu'))
@pytest.mark.usefixtures('fake_vhosts_for_user')
def test_get_vhost_failure(domain):
    assert _get_vhost('ckuehl', domain) is None


@pytest.fixture
def fake_vhost():
    return mock.Mock(**{'get_forwarding_addresses.return_value': [
        mock.Mock(address='ckuehl@ocf.berkeley.edu'),
        mock.Mock(address='a@gmail.com'),
    ]})


@pytest.mark.parametrize('addr', ('ckuehl@ocf.berkeley.edu', 'a@gmail.com'))
def test_find_addr_success(addr, fake_vhost):
    assert _find_addr(mock.Mock(), fake_vhost, addr).address == addr


@pytest.mark.parametrize('addr', ('b@gmail.com', '@ocf.berkeley.edu'))
def test_find_addr_failure(addr, fake_vhost):
    assert _find_addr(mock.Mock(), fake_vhost, addr) is None


@pytest.yield_fixture
def fake_cursor():
    cursor = mock.Mock()

    @contextmanager
    def side_effect(**kwargs):
        assert kwargs['autocommit'] is False
        yield cursor

    with mock.patch.object(vhost_mail, 'get_connection', side_effect=side_effect):
        yield cursor


def test_txn_commits_on_success(fake_cursor):
    with _txn():
        pass
    fake_cursor.connection.commit.assert_called_once()
    assert not fake_cursor.connection.rollback.called


def test_txn_rolls_back_and_raises_on_failure(fake_cursor):
    with pytest.raises(ValueError):
        with _txn():
            raise ValueError('lol sup')
    fake_cursor.connection.rollback.assert_called_once()
    assert not fake_cursor.connection.commit.called
