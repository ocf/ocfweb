from contextlib import contextmanager

import mock
import pytest
from django.contrib import messages
from django.http import HttpResponseRedirect

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
