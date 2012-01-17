import pexpect
import os
import base64
import ldap

from django.conf import settings

def _clean_user_account(user_account):
    return "".join(filter(lambda char: char.islower(), [char for char in user_account]))

def _ad_unicode_password(raw_password):
    raw_password = "\"%s\"" % raw_password
    raw_password = raw_password.encode("latin1", "ignore")
    return unicode(raw_password).encode("utf-16-le")
    
def _people_dn(account_name):
    return "CN=%s,OU=People,DC=lab,DC=ocf,DC=berkeley,DC=edu" % account_name

def _staff_dn(account_name):
    return "CN=%s,OU=Staff,DC=lab,DC=ocf,DC=berkeley,DC=edu" % account_name

def change_ad_password(user_account, new_password):
    ldap_password = open(settings.AD_PASSWORD_FILE, "r").read().strip()
    ldap.set_option(ldap.OPT_X_TLS_CACERTFILE, settings.AD_CACERTFILE)
    ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
    ldap.set_option(ldap.OPT_REFERRALS,0)

    l = ldap.initialize("ldaps://biohazard.ocf.berkeley.edu")
    l.simple_bind_s(_staff_dn(settings.AD_USERNAME), ldap_password)

    modlist = [(ldap.MOD_REPLACE, "userAccountControl", "66048"),
        (ldap.MOD_REPLACE, "unicodePwd", _ad_unicode_password(new_password))]
    
    return l.modify_s(_people_dn(_clean_user_account(user_account)), modlist)

def _kadmin_command(user_account):
    return "%(kadmin_location)s -K %(kerberos_keytab)s -p %(kerberos_principal)s cpw %(user_account)s" % {
            "kadmin_location": settings.KADMIN_LOCATION,
            "kerberos_keytab": settings.KRB_KEYTAB,
            "kerberos_principal": settings.KRB_PRINCIPAL,
            "user_account": _clean_user_account(user_account)
        }

def change_krb_password(user_account, new_password):
    cmd = _kadmin_command(user_account)
    child = pexpect.spawn(cmd, timeout=10)
    
    child.expect("%s@OCF.BERKELEY.EDU's Password:" % user_account)
    child.sendline(new_password)

    child.expect("Verifying - %s@OCF.BERKELEY.EDU's Password:" % user_account)
    child.sendline(new_password)
    
    child.expect(".*")

    return [not child.isalive(), child.before, child.after]
