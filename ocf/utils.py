import ldap
from django.conf import settings

def users_by_calnet_uid(calnet_uid):
    l = ldap.initialize(settings.OCF_LDAP)
    l.simple_bind_s("","")

    search_filter = "(berkeleyEduCalNetUID=%s)" % calnet_uid
    attrs = ["uid"]

    ldap_entries = l.search_st("ou=People,dc=OCF,dc=Berkeley,dc=EDU", ldap.SCOPE_SUBTREE, search_filter, attrs)

    return [entry[1]["uid"][0] for entry in ldap_entries]
