import ldap
from django.conf import settings

def clean_user_account(user_account):
    """Return an string that could be an OCF user name"""

    if not user_account:
        return ""

    return "".join(filter(lambda char: char.islower(), [char for char in user_account]))

def clean_password(password):
    """Return a string without tab or newlines"""

    if not password:
        return ""

    return "".join(filter(lambda char: char not in ["\t", "\n"], [char for char in password]))

def users_by_calnet_uid(calnet_uid):
    """Get a list of users associated with a CalNet UID"""

    l = ldap.initialize(settings.OCF_LDAP)
    l.simple_bind_s("", "")

    search_filter = "(berkeleyEduCalNetUID=%s)" % calnet_uid
    attrs = ["uid"]

    ldap_entries = l.search_st("ou=People,dc=OCF,dc=Berkeley,dc=EDU", ldap.SCOPE_SUBTREE, search_filter, attrs)

    return [entry[1]["uid"][0] for entry in ldap_entries]

def user_exists(user_account):
    """Returns True if an OCF user exists with specified account name"""

    l = ldap.initialize(settings.OCF_LDAP)
    l.simple_bind_s("", "")

    search_filter = "(uid=%s)" % user_account
    attrs = []
    ldap_entries = l.search_st("ou=People,dc=OCF,dc=Berkeley,dc=EDU", ldap.SCOPE_SUBTREE, search_filter, attrs)

    return len(ldap_entries) == 1
