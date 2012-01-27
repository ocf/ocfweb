import ldap
from django.conf import settings

def clean_user_account(user_account):
    return "".join(filter(lambda char: char.islower(), [char for char in user_account]))

def clean_password(password):
    return "".join(filter(lambda char: char not in ["\t", "\n"], [char for char in password]))

def users_by_calnet_uid(calnet_uid):
    l = ldap.initialize(settings.OCF_LDAP)
    l.simple_bind_s("", "")

    search_filter = "(berkeleyEduCalNetUID=%s)" % calnet_uid
    attrs = ["uid"]

    ldap_entries = l.search_st("ou=People,dc=OCF,dc=Berkeley,dc=EDU", ldap.SCOPE_SUBTREE, search_filter, attrs)

    return [entry[1]["uid"][0] for entry in ldap_entries]

def user_exists(user_account):
    l = ldap.initialize(settings.OCF_LDAP)
    l.simple_bind_s("", "")

    search_filter = "(uid=%s)" % user_account
    attrs = []
    ldap_entries = l.search_st("ou=People,dc=OCF,dc=Berkeley,dc=EDU", ldap.SCOPE_SUBTREE, search_filter, attrs)

    return len(ldap_entries) == 1
