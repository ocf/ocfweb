import sys
import ldap
import pexpect
from re import match
from django.conf import settings
from dns import resolver

def clean_user_account(user_account):
    """Return an string that could be an OCF user name"""

    if not user_account:
        return ""

    return "".join(filter(lambda c: c.islower(), [c for c in user_account]))


def clean_password(password):
    """Return a string without tab or newlines"""

    if not password:
        return ""

    password = password.replace("\t", "")
    password = password.replace("\n", "")

    return password


def users_by_calnet_uid(calnet_uid):
    """Get a list of users associated with a CalNet UID"""

    l = ldap.initialize(settings.OCF_LDAP)
    l.simple_bind_s("", "")

    search_filter = "(calnetUid=%s)" % calnet_uid
    attrs = ["uid"]

    ldap_entries = l.search_st("ou=People,dc=OCF,dc=Berkeley,dc=EDU",
                               ldap.SCOPE_SUBTREE, search_filter, attrs)

    return [entry[1]["uid"][0] for entry in ldap_entries]

def user_attrs(user_account):
    """Returns a dictionary of LDAP attributes for a given LDAP UID in
    the form:

    {
      'uid': ['somebody'],
      'objectClass': ['ocfAccount', 'account', 'posixAccount'],
      'loginShell': ['/bin/zsh']
    }

    Returns None if no account exists with uid=user_account.
    """

    l = ldap.initialize(settings.OCF_LDAP)
    l.simple_bind_s("", "")

    search_filter = "(uid=%s)" % user_account

    ldap_entries = l.search_st("ou=People,dc=OCF,dc=Berkeley,dc=EDU",
                               ldap.SCOPE_SUBTREE, search_filter)

    if len(ldap_entries) > 0:
        return ldap_entries[0][1]

def user_is_group(user_account):
    """Returns True if an OCF user account exists and is a group account"""

    attrs = user_attrs(user_account)
    if 'callinkOid' in attrs or 'oslGid' in attrs:
        return True

def user_exists(user_account):
    """Returns True if an OCF user exists with specified account name"""

    l = ldap.initialize(settings.OCF_LDAP)
    l.simple_bind_s("", "")

    search_filter = "(uid=%s)" % user_account
    attrs = []
    ldap_entries = l.search_st("ou=People,dc=OCF,dc=Berkeley,dc=EDU",
                               ldap.SCOPE_SUBTREE, search_filter, attrs)

    return len(ldap_entries) == 1

def password_matches(user_account, password):
    """Returns True if the password matches the user account given"""

    user_account = clean_user_account(user_account)
    password = clean_password(password)

    cmd = "kinit --no-forwardable -l0 %s@OCF.BERKELEY.EDU" % user_account
    child = pexpect.spawn(cmd, timeout=10)

    child.expect("%s@OCF.BERKELEY.EDU's Password:" % user_account)
    child.sendline(password)

    child.expect(pexpect.EOF)
    child.close()

    return child.exitstatus == 0

def check_email(email):
    """
    Check the email with naive regex and check for the domain's MX record.
    Returns True for valid email, False for bad email.
    """
    regex = r'^[a-zA-Z0-9._%\-+]+@([a-zA-Z0-9._%\-]+.[a-zA-Z]{2,6})$'

    m = match(regex, email)
    if m:
        domain = m.group(1)
        try:
            # Check that the domain has MX record(s)
            answer = resolver.query(domain, 'MX')
            if answer:
                return True
        except (resolver.NoAnswer, resolver.NXDOMAIN):
            pass
    return False
