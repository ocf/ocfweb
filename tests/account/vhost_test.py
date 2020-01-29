import pytest

from ocfweb.account.vhost import available_domain
from ocfweb.account.vhost import valid_domain_external


@pytest.mark.parametrize(
    'domain,expected', [
        # nxdomain (should be available)
        ('asdfghjk.berkeley.edu', True),
        ('kljasdlgjlsafdfhsadf.berkeley.edu', True),

        # mx record only
        ('g.berkeley.edu', False),

        # a record
        ('dev-ocf.berkeley.edu', False),

        # cname
        ('mirrors.berkeley.edu', False),

        # existing domains
        ('ocf.berkeley.edu', False),
        ('cs.berkeley.edu', False),

        # existing subdomains
        ('cory.eecs.berkeley.edu', False),

        # non-existing subdomains
        ('asdfghjkl.eecs.berkeley.edu', False),

        # nonsense
        ('berkeley.edu', False),
        ('.berkeley.edu', False),
        ('jf0194y89v(*#14o1i9XC', False),
        ('@I$)!($U)!#Y%!)#()*(%!#', False),
        ('vns;alf iashf poasf bawen svn;', False),
    ],
)
def test_available_domain(domain, expected):
    assert available_domain(domain) is expected


@pytest.mark.parametrize(
    'domain,expected', [
        # any proper domain goes
        ('ocf.berkeley.edu', True),
        ('example.com', True),

        # malformatted domains
        ('edu', False),
        ('.io', False),
        ('www..com', False),
    ],
)
def test_valid_domain_external(domain, expected):
    assert valid_domain_external(domain) is expected
