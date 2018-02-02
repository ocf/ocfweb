import crypt
import csv
import io
import re
from contextlib import contextmanager
from datetime import datetime
from textwrap import dedent
from unittest import mock

import pytest
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
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
from ocfweb.account.vhost_mail import _parse_csv
from ocfweb.account.vhost_mail import _parse_csv_forward_addrs
from ocfweb.account.vhost_mail import _redirect_back
from ocfweb.account.vhost_mail import _txn
from ocfweb.account.vhost_mail import _write_csv
from ocfweb.account.vhost_mail import EXAMPLE_CSV
from ocfweb.account.vhost_mail import REMOVE_PASSWORD
from ocfweb.component.errors import ResponseException


TEST_VIEWS = (
    ('vhost_mail', ()),
    ('vhost_mail_update', ()),
    ('vhost_mail_csv_export', ('vhost.com',)),
    ('vhost_mail_csv_import', ('vhost.com',)),
)


@pytest.mark.parametrize('view', TEST_VIEWS)
def test_view_requires_login(view, client):
    """Logged out users should get redirected to login."""
    name, args = view
    resp = client.get(reverse(name, args=args))
    assert resp.status_code == 302
    assert resp.url == reverse('login')


@pytest.mark.parametrize('view', TEST_VIEWS)
def test_view_requires_group_account(view, client_guser):
    """Individual accounts should get an error."""
    name, args = view
    resp = client_guser.get(reverse(name, args=args))
    assert resp.status_code == 403


def test_main_view_works(client_ggroup):
    """Smoke test with a valid user."""
    fake_vhosts = {
        mock.Mock(
            user='ggroup',
            domain='vhost.com',
            **{
                'get_forwarding_addresses.return_value': {
                    MailForwardingAddress(
                        address='bob@vhost.com',
                        crypt_password=None,
                        forward_to=frozenset(('a@gmail.com', 'b@gmail.com')),
                        last_updated=datetime.now(),
                    ),
                },
            },
        ),
    }
    with mock.patch.object(vhost_mail, 'vhosts_for_user', return_value=fake_vhosts):
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
        MailForwardingAddress(
            address='another@vhost.com',
            crypt_password=None,
            forward_to=frozenset(('someguy@gmail.com',)),
            last_updated=datetime(2000, 1, 1),
        ),
    }
    with mock.patch.object(
        vhost_mail, 'vhosts_for_user', return_value={
            mocked_vhost, mocked_vhost2,
        },
    ):
        yield mocked_vhost


@pytest.yield_fixture
def mock_txn():
    with mock.patch.object(vhost_mail, '_txn') as m:
        yield m


@pytest.yield_fixture
def mock_messages():
    with mock.patch.object(vhost_mail.messages, 'add_message') as m:
        yield m


class VerifyPassword:

    def __init__(self, password):
        self.password = password

    def __eq__(self, other):
        if self.password is None:
            return other is None
        else:
            return crypt.crypt(self.password, salt=other)


@pytest.mark.parametrize(
    ('addr', 'password', 'expected_password'), (
        ('john@vhost.com', 'nice password bro', VerifyPassword('nice password bro')),
        ('@vhost.com', 'nice password bro', VerifyPassword(None)),
        ('@vhost.com', None, VerifyPassword(None)),
    ),
)
def test_update_add_new_addr(
        addr,
        password,
        expected_password,
        client_ggroup,
        mock_ggroup_vhost,
        mock_messages,
        mock_txn,
):
    resp = client_ggroup.post(
        reverse('vhost_mail_update'), {
            'action': 'add',
            'addr': addr,
            'forward_to': 'john@gmail.com,bob@gmail.com',
            'password': 'nice password bro',
        },
    )
    mock_ggroup_vhost.add_forwarding_address.assert_called_once_with(
        mock_txn().__enter__(),
        MailForwardingAddress(
            address=addr,
            forward_to=frozenset(('john@gmail.com', 'bob@gmail.com')),
            crypt_password=expected_password,
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
    resp = client_ggroup.post(
        reverse('vhost_mail_update'), {
            'action': 'add',
            'addr': 'exists@vhost.com',
            'forward_to': 'john@gmail.com,bob@gmail.com',
            'password': 'nice password bro',
        },
    )
    assert not mock_ggroup_vhost.add_forwarding_address.called
    assert resp.status_code == 302
    mock_messages.assert_called_once_with(
        mock.ANY,
        messages.ERROR,
        'The address "exists@vhost.com" already exists!',
    )


def test_update_fails_to_add_addr_to_bad_vhost(client_ggroup, mock_ggroup_vhost, mock_messages, mock_txn):
    resp = client_ggroup.post(
        reverse('vhost_mail_update'), {
            'action': 'add',
            'addr': 'john@bad-vhost.com',
            'forward_to': 'john@gmail.com,bob@gmail.com',
            'password': 'nice password bro',
        },
    )
    assert not mock_ggroup_vhost.add_forwarding_address.called
    assert resp.status_code == 302
    mock_messages.assert_called_once_with(
        mock.ANY,
        messages.ERROR,
        'You cannot use the domain: "bad-vhost.com"',
    )


def test_update_delete_addr(client_ggroup, mock_ggroup_vhost, mock_messages, mock_txn):
    resp = client_ggroup.post(
        reverse('vhost_mail_update'), {
            'action': 'delete',
            'addr': 'exists@vhost.com',
        },
    )
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
    resp = client_ggroup.post(
        reverse('vhost_mail_update'), {
            'action': 'delete',
            'addr': 'john@vhost.com',
        },
    )
    assert not mock_ggroup_vhost.add_forwarding_address.called
    assert not mock_ggroup_vhost.remove_forwarding_address.called
    assert resp.status_code == 302
    mock_messages.assert_called_once_with(
        mock.ANY,
        messages.ERROR,
        'The address "john@vhost.com" does not exist!',
    )


def test_update_replace_some_stuff(client_ggroup, mock_ggroup_vhost, mock_messages, mock_txn):
    resp = client_ggroup.post(
        reverse('vhost_mail_update'), {
            'action': 'update',
            'addr': 'exists@vhost.com',
            'new_addr': 'john@vhost.com',
            'forward_to': 'john@gmail.com,bob@gmail.com',
            'password': 'nice password bro',
        },
    )
    mock_ggroup_vhost.remove_forwarding_address.assert_called_once_with(
        mock_txn().__enter__(),
        'exists@vhost.com',
    )
    mock_ggroup_vhost.add_forwarding_address.assert_called_once_with(
        mock_txn().__enter__(),
        MailForwardingAddress(
            address='john@vhost.com',
            forward_to=frozenset(('john@gmail.com', 'bob@gmail.com')),
            crypt_password=VerifyPassword('nice password bro'),
            last_updated=mock.ANY,
        ),
    )
    assert resp.status_code == 302
    mock_messages.assert_called_once_with(
        mock.ANY,
        messages.SUCCESS,
        'Update successful!',
    )


def test_update_remove_password(client_ggroup, mock_ggroup_vhost, mock_messages, mock_txn):
    resp = client_ggroup.post(
        reverse('vhost_mail_update'), {
            'action': 'update',
            'addr': 'exists@vhost.com',
            'password': '',
        },
    )
    mock_ggroup_vhost.remove_forwarding_address.assert_called_once_with(
        mock_txn().__enter__(),
        'exists@vhost.com',
    )
    mock_ggroup_vhost.add_forwarding_address.assert_called_once_with(
        mock_txn().__enter__(),
        MailForwardingAddress(
            address='exists@vhost.com',
            forward_to=frozenset(('tom@gmail.com', 'bob@gmail.com')),
            crypt_password=None,
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
    resp = client_ggroup.post(
        reverse('vhost_mail_update'), {
            'action': 'update',
            'addr': 'exists@vhost.com',
        },
    )
    mock_ggroup_vhost.remove_forwarding_address.assert_called_once_with(
        mock_txn().__enter__(),
        'exists@vhost.com',
    )
    mock_ggroup_vhost.add_forwarding_address.assert_called_once_with(
        mock_txn().__enter__(),
        MailForwardingAddress(
            address='exists@vhost.com',
            forward_to=frozenset(('bob@gmail.com', 'tom@gmail.com')),
            crypt_password='crypt',
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
    resp = client_ggroup.post(
        reverse('vhost_mail_update'), {
            'action': 'update',
            'addr': 'john@vhost.com',
            'password': 'some great password',
        },
    )
    assert not mock_ggroup_vhost.add_forwarding_address.called
    assert not mock_ggroup_vhost.remove_forwarding_address.called
    assert resp.status_code == 302
    mock_messages.assert_called_once_with(
        mock.ANY,
        messages.ERROR,
        'The address "john@vhost.com" does not exist!',
    )


@pytest.mark.parametrize(
    'forward_to,expected_error', (
        ('', 'You must provide at least one address to forward to!'),
        ('@gmail.com', 'Invalid forwarding address: "@gmail.com"'),
        ('bob@gmail.com,@berkeley.edu', 'Invalid forwarding address: "@berkeley.edu"'),
    ),
)
def test_update_replace_addr_bad_forward_to(
        forward_to,
        expected_error,
        client_ggroup,
        mock_ggroup_vhost,
        mock_messages,
        mock_txn,
):
    resp = client_ggroup.post(
        reverse('vhost_mail_update'), {
            'action': 'update',
            'addr': 'john@vhost.com',
            'forward_to': forward_to,
        },
    )
    assert not mock_ggroup_vhost.add_forwarding_address.called
    assert not mock_ggroup_vhost.remove_forwarding_address.called
    assert resp.status_code == 302
    mock_messages.assert_called_once_with(
        mock.ANY,
        messages.ERROR,
        expected_error,
    )


def test_update_cant_move_addr_across_vhosts(client_ggroup, mock_ggroup_vhost, mock_messages, mock_txn):
    resp = client_ggroup.post(
        reverse('vhost_mail_update'), {
            'action': 'update',
            'addr': 'john@vhost.com',
            'new_addr': 'john@vhost2.com',
        },
    )
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


@pytest.mark.parametrize(
    ('addr', 'expected'), [
        ('ckuehl@ocf.berkeley.edu', ('ckuehl', 'ocf.berkeley.edu')),
        ('ckuehl+yolo1._2+3@ocf.berkeley.edu', ('ckuehl+yolo1._2+3', 'ocf.berkeley.edu')),
        ('a@a.a', ('a', 'a.a')),
    ],
)
@pytest.mark.parametrize('allow_wildcard', (True, False))
def test_parse_addr_success(addr, expected, allow_wildcard):
    assert _parse_addr(addr, allow_wildcard=allow_wildcard) == expected


@pytest.mark.parametrize(
    'addr', [
        'ckuehl',
        '',
        '   ',
        '\t',
        ' ckuehl@ocf.berkeley.edu',
        'ckuehl\t@ocf.berkeley.edu',
        'ckuehl@',
        '@',
        'asdf@asdf',
        '@wat',
    ],
)
@pytest.mark.parametrize('allow_wildcard', (True, False))
def test_parse_addr_invalid(addr, allow_wildcard):
    assert _parse_addr(addr, allow_wildcard=allow_wildcard) is None


@pytest.mark.parametrize(
    'addr', (
        '@ocf.berkeley.edu',
        '@vhost.com',
        '@a-b-c.e.f-gh.net',
    ),
)
def test_parse_addr_wildcards(addr):
    assert _parse_addr(addr) is None
    assert _parse_addr(addr, allow_wildcard=True) == (None, addr[1:])


@pytest.mark.parametrize(
    ('addr', 'name', 'domain'), (
        ('ckuehl@ocf.berkeley.edu', 'ckuehl', 'ocf.berkeley.edu'),
        ('john.doe+test@gmail.com', 'john.doe+test', 'gmail.com'),
        ('@gmail.com', None, 'gmail.com'),

        # people suck at forms
        (' \t  ckuehl@ocf.berkeley.edu', 'ckuehl', 'ocf.berkeley.edu'),
    ),
)
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


@pytest.mark.parametrize(
    ('addr', 'domain'), (
        ('ckuehl@ocf.berkeley.edu', 'ocf.berkeley.edu'),
        ('john.doe+test@gmail.com', 'gmail.com'),
    ),
)
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


@pytest.mark.parametrize(
    ('forward_to', 'expected'), (
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
    ),
)
def test_get_forward_to_valid(forward_to, expected):
    result = _get_forward_to(fake_request(forward_to=forward_to))
    assert result == expected


@pytest.mark.parametrize('forward_to', ('', ',    , , , ', '\n', '    '))
def test_get_forward_to_no_addrs_provided(forward_to, fake_error):
    with pytest.raises(fake_error) as ex:
        _get_forward_to(fake_request(forward_to=forward_to))
    assert ex.value.args[0] == 'You must provide at least one address to forward to!'


@pytest.mark.parametrize(
    ('forward_to', 'first_invalid'), (
        ('a@a,b@gmail.com', 'a@a'),
        ('a@a,b', 'a@a'),
        ('asdf@gmail.com, ,   ,john.doe,boo@gmail.com', 'john.doe'),
    ),
)
def test_get_forward_to_invalid_addrs_provided(forward_to, first_invalid, fake_error):
    with pytest.raises(fake_error) as ex:
        _get_forward_to(fake_request(forward_to=forward_to))
    assert ex.value.args[0] == 'Invalid forwarding address: "{}"'.format(first_invalid)


def test_get_password_no_name():
    assert _get_password(fake_request(password='password'), None) is REMOVE_PASSWORD


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


def test_get_password_not_present():
    """If "password" is not present, just do nothing."""
    assert _get_password(fake_request(), 'ckuehl') is None


def test_get_password_empty():
    """If password is present and an empty string, remove it."""
    assert _get_password(fake_request(password=''), 'ckuehl') is REMOVE_PASSWORD


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
    fake_cursor.connection.commit.assert_called_once_with()
    assert not fake_cursor.connection.rollback.called


def test_txn_rolls_back_and_raises_on_failure(fake_cursor):
    with pytest.raises(ValueError):
        with _txn():
            raise ValueError('lol sup')
    fake_cursor.connection.rollback.assert_called_once_with()
    assert not fake_cursor.connection.commit.called


@pytest.mark.parametrize(
    'addrs,expected', (
        ('a@a.a', {'a@a.a'}),
        ('a@a.a b@b.b', {'a@a.a', 'b@b.b'}),
        ('a@a.a, b@b.b, ', {'a@a.a', 'b@b.b'}),
        ('a@a.a, \t\n,b@b.b', {'a@a.a', 'b@b.b'}),
    ),
)
def test_parse_csv_forward_addrs_success(addrs, expected):
    """Comma/whitespace separated lists of valid email addresses work."""
    assert _parse_csv_forward_addrs(addrs) == expected


@pytest.mark.parametrize(
    'addrs', (
        '',
        ', \t\r\n',
        'invalid',
        'valid@email.address invalid-email-address',
    ),
)
def test_parse_csv_forward_addrs_failure(addrs):
    """Empty lists and lists with invalid email addresses fail."""
    with pytest.raises(ValueError):
        _parse_csv_forward_addrs(addrs)


def test_parse_csv_example_success():
    """The on-page example is actually valid."""
    csv_file = io.BytesIO(bytes(EXAMPLE_CSV, encoding='utf-8'))
    fake_request = mock.Mock(**{'FILES.get': {'csv_file': csv_file}.get})
    john_doe, jane_doe = 'john.doe@berkeley.edu', 'jane.doe@berkeley.edu'
    assert _parse_csv(fake_request, 'example.com') == {
        'president@example.com': {john_doe},
        'officers@example.com': {john_doe, jane_doe},
        'committee@example.com': {john_doe, jane_doe},
        'members@example.com': {john_doe, jane_doe},
    }


@pytest.mark.parametrize(
    'csv_text', (
        'toofew',
        'too,many,',
        'invalid@example.com,',
        'valid,invalid@example@com',
        'valid,valid@example.com invalid',
    ),
)
def test_parse_csv_failure(csv_text, fake_error):
    """CSV with wrong # of columns or invalid email addresses fails."""
    csv_file = io.BytesIO(bytes(csv_text, encoding='utf-8'))
    fake_request = mock.Mock(**{'FILES.get': {'csv_file': csv_file}.get})
    with pytest.raises(fake_error):
        _parse_csv(fake_request, 'vhost.com')


def test_write_csv_has_correct_format(mock_ggroup_vhost):
    """Output CSV has two columns and valid email addresses."""
    f = io.StringIO(_write_csv(mock_ggroup_vhost.get_forwarding_addresses()))
    reader = csv.reader(f)
    for row in reader:
        assert len(row) == 2
        assert _parse_addr(row[0] + '@' + mock_ggroup_vhost.domain)
        assert _parse_csv_forward_addrs(row[1])


def check_csv_has_addresses(csv_str, addresses):
    """A helper for roughly checking the contents of a CSV document."""
    for addr in addresses:
        m = re.search(addr.address.split('@')[0] + r'.*$', csv_str, re.MULTILINE)
        assert m
        s = m.group(0)
        for to_addr in addr.forward_to:
            assert re.search(to_addr, s)


def test_write_csv_has_expected_rows(mock_ggroup_vhost):
    """Output CSV has all email addresses from the vhost."""
    addresses = mock_ggroup_vhost.get_forwarding_addresses()
    csv_str = _write_csv(addresses)
    check_csv_has_addresses(csv_str, addresses)


def test_parse_then_write_csv_is_noop(mock_ggroup_vhost):
    """Not an explicit goal, but write-parse-write should be the same
    as one write de facto if our data structures are consistent."""
    addresses_1 = mock_ggroup_vhost.get_forwarding_addresses()
    csv_str_1 = _write_csv(addresses_1)
    f = io.BytesIO(bytes(csv_str_1, encoding='utf-8'))
    fake_request = mock.Mock(**{'FILES.get': {'csv_file': f}.get})
    addresses_2 = frozenset({
        MailForwardingAddress(
            address=from_addr,
            forward_to=to_addrs,
            crypt_password=None,
            last_updated=None,
        )
        for from_addr, to_addrs in _parse_csv(fake_request, 'vhost.com').items()
    })
    assert _write_csv(addresses_2)


def test_import_csv_success(client_ggroup, mock_ggroup_vhost, mock_messages, mock_txn):
    """A test request that adds and updates addresses should work and
    preserve passwords."""
    csv_text = dedent("""\
        exists,bub@gmail.com tim@gmail.com
        newtestaddress,someone@example.com
    """)
    resp = client_ggroup.post(
        reverse('vhost_mail_csv_import', args=('vhost.com',)),
        {
            'csv_file': io.StringIO(csv_text),
        },
    )
    mock_ggroup_vhost.remove_forwarding_address.assert_called_once_with(
        mock_txn().__enter__(),
        'exists@vhost.com',
    )
    mock_ggroup_vhost.add_forwarding_address.assert_has_calls(
        any_order=True, calls=(
            mock.call(
                mock_txn().__enter__(),
                MailForwardingAddress(
                    address='exists@vhost.com',
                    crypt_password='crypt',
                    forward_to=frozenset(('bub@gmail.com', 'tim@gmail.com')),
                    last_updated=None,
                ),
            ),
            mock.call(
                mock_txn().__enter__(),
                MailForwardingAddress(
                    address='newtestaddress@vhost.com',
                    forward_to=frozenset(('someone@example.com',)),
                    crypt_password=None,
                    last_updated=None,
                ),
            ),
        ),
    )
    assert resp.status_code == 302
    mock_messages.assert_called_once_with(
        mock.ANY,
        messages.SUCCESS,
        'Import successful!',
    )


def test_import_noop_csv(client_ggroup, mock_ggroup_vhost, mock_messages, mock_txn):
    """Exporting then importing ideally doesn't even hit the
    database."""
    csv_text = _write_csv(mock_ggroup_vhost.get_forwarding_addresses())
    resp = client_ggroup.post(
        reverse('vhost_mail_csv_import', args=('vhost.com',)),
        {
            'csv_file': io.StringIO(csv_text),
        },
    )
    assert not mock_ggroup_vhost.remove_forwarding_address.called
    assert not mock_ggroup_vhost.add_forwarding_address.called
    assert resp.status_code == 302
    mock_messages.assert_called_once_with(
        mock.ANY,
        messages.SUCCESS,
        'Import successful!',
    )


def test_import_empty_csv(client_ggroup, mock_ggroup_vhost, mock_messages, mock_txn):
    """The parser doesn't reject an empty CSV, so it must pass."""
    resp = client_ggroup.post(
        reverse('vhost_mail_csv_import', args=('vhost.com',)),
        {
            'csv_file': io.StringIO(''),
        },
    )
    assert not mock_ggroup_vhost.remove_forwarding_address.called
    assert not mock_ggroup_vhost.add_forwarding_address.called
    assert resp.status_code == 302
    mock_messages.assert_called_once_with(
        mock.ANY,
        messages.SUCCESS,
        'Import successful!',
    )


def test_import_csv_missing(client_ggroup, mock_ggroup_vhost, mock_messages, mock_txn):
    """POSTing to the CSV import URL without a CSV file fails."""
    resp = client_ggroup.post(reverse('vhost_mail_csv_import', args=('nonexist.com',)))
    assert resp.status_code == 302
    mock_messages.assert_called_once_with(
        mock.ANY,
        messages.ERROR,
        mock.ANY,
    )


def test_import_csv_bad_vhost_fails(client_ggroup, mock_ggroup_vhost, mock_messages, mock_txn):
    """POSTing to the CSV import URL for an unowned domain fails."""
    resp = client_ggroup.post(
        reverse('vhost_mail_csv_import', args=('nonexist.com',)),
        {
            'csv_file': io.StringIO('address,test@example.com'),
        },
    )
    assert not mock_ggroup_vhost.remove_forwarding_address.called
    assert not mock_ggroup_vhost.add_forwarding_address.called
    assert resp.status_code == 302
    mock_messages.assert_called_once_with(
        mock.ANY,
        messages.ERROR,
        'You cannot use the domain: "nonexist.com"',
    )


@pytest.mark.parametrize(
    ('csv_str', 'expected_err'), (
        ('email', 'Must have exactly 2 columns'),
        (',,', 'Must have exactly 2 columns'),
        (',', 'Invalid forwarding address: "@vhost.com"'),
        ('invalid@vhost.com,', 'Invalid forwarding address: "invalid@vhost.com@vhost.com"'),
        ('email,', 'Missing forward-to address'),
        ('email,invalid', 'Invalid address: "invalid"'),
        ('email,valid@example.com invalid', 'Invalid address: "invalid"'),
    ),
)
def test_import_invalid_csv_fails(csv_str, expected_err, client_ggroup, mock_ggroup_vhost, mock_messages, mock_txn):
    """Trying to import malformatted CSV fails."""
    resp = client_ggroup.post(
        reverse('vhost_mail_csv_import', args=('vhost.com',)),
        {
            'csv_file': io.StringIO(csv_str),
        },
    )
    assert not mock_ggroup_vhost.remove_forwarding_address.called
    assert not mock_ggroup_vhost.add_forwarding_address.called
    assert resp.status_code == 302
    mock_messages.assert_called_once_with(
        mock.ANY,
        messages.ERROR,
        'Error parsing CSV: row 1: ' + expected_err,
    )


def test_export_csv_works(client_ggroup, mock_ggroup_vhost, mock_txn):
    """Exporting CSV from a valid domain gives the expected data."""
    resp = client_ggroup.get(reverse('vhost_mail_csv_export', args=('vhost.com',)))
    assert resp.status_code == 200
    check_csv_has_addresses(
        str(resp.content, encoding='utf-8'),
        mock_ggroup_vhost.get_forwarding_addresses(),
    )


def test_export_csv_bad_vhost_fails(client_ggroup, mock_ggroup_vhost, mock_txn, mock_messages):
    """Hitting the CSV export URL for an unowned domain fails."""
    resp = client_ggroup.get(reverse('vhost_mail_csv_export', args=('nonexist.com',)))
    assert resp.status_code == 302
    mock_messages.assert_called_once_with(
        mock.ANY,
        messages.ERROR,
        'You cannot use the domain: "nonexist.com"',
    )
