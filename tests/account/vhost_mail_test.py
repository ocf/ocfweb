import pytest

from ocfweb.account.vhost_mail import _parse_addr


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
])
def test_parse_addr_failure(addr):
    assert _parse_addr(addr) is None
