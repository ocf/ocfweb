import pexpect
import os
import base64
import time
from django.conf import settings
from ocf.utils import clean_user_account, clean_password

def _ad_unicode_password(raw_password):
    """Returns a password in a format that Active Directory will accept"""

    raw_password = "\"%s\"" % raw_password
    raw_password = raw_password.encode("latin1", "ignore")
    return unicode(raw_password).encode("utf-16-le")
    
def _people_dn(account_name):
    return "CN=%s,OU=People,DC=lab,DC=ocf,DC=berkeley,DC=edu" % account_name

def _staff_dn(account_name):
    return "CN=%s,OU=Staff,DC=lab,DC=ocf,DC=berkeley,DC=edu" % account_name

def _ldapmodify_command():
    return "ldapmodify -x -H %(ad_host)s -D %(staff_dn)s -y %(ldap_password_file)s" % {
            "ad_host": settings.AD_HOST,
            "staff_dn": _staff_dn(settings.AD_USERNAME),
            "ldap_password_file": settings.AD_PASSWORD_FILE
        }

def change_ad_password(user_account, new_password):
    """Change a user's Active Directory password.

    Runs an ldapmodify command in a pexpect session to change a user's password.

    Args:
        user_account: a dirty string of a user's OCF account
        new_password: a dirty string of a user's new password

    Returns:
        True if successful

    Raises:
        pexpect.TIMEOUT: We never got the line that we were expecting,
            so something probably went wrong with the lines that we sent.
        pexpect.EOF: The child ended prematurely.

    """

    user_account = clean_user_account(user_account)
    new_password = clean_password(new_password)
    cmd = _ldapmodify_command()
    child = pexpect.spawn(cmd, timeout=10, env={"LDAPCONF": "/opt/ocf/packages/account/chpass/ldap.conf"})

    dn = _people_dn(user_account)

    child.sendline("dn: %s" % dn)
    child.sendline("changetype: modify")
    child.sendline("replace: unicodePwd")
    base64_password = base64.b64encode(_ad_unicode_password(new_password))
    child.sendline("unicodePwd::%s" % base64_password)
    child.send("\n\n")
    child.expect("modifying entry")

    child.sendeof()
    child.expect(pexpect.EOF)

    return True

def _kadmin_command(user_account):
    user_account = clean_user_account(user_account)
    return "%(kadmin_location)s -K %(kerberos_keytab)s -p %(kerberos_principal)s cpw %(user_account)s" % {
            "kadmin_location": settings.KADMIN_LOCATION,
            "kerberos_keytab": settings.KRB_KEYTAB,
            "kerberos_principal": settings.KRB_PRINCIPAL,
            "user_account": user_account
        }

def change_krb_password(user_account, new_password):
    """"Change a user's Kerberos password.

    Runs a kadmin command in a pexpect session to change a user's password.

    Args:
        user_account: a dirty string of a user's OCF account
        new_password: a dirty string of a user's new password

    Returns:
        True if successful

    Raises:
        Exception: kadmin returned an error. Probably incorrect
            principal or error with sending the new password.
        pexpect.TIMEOUT: We never got the line that we were expecting,
            so something probably went wrong with the lines that we sent.
        pexpect.EOF: The child ended prematurely.

    """

    user_account = clean_user_account(user_account)
    new_password = clean_password(new_password)
    cmd = _kadmin_command(user_account)
    child = pexpect.spawn(cmd, timeout=10)
    
    child.expect("%s@OCF.BERKELEY.EDU's Password:" % user_account)
    child.sendline(new_password)

    child.expect("Verifying - %s@OCF.BERKELEY.EDU's Password:" % user_account)
    child.sendline(new_password)
    
    child.expect(pexpect.EOF)
    if "kadmin" in child.before:
        raise Exception("kadmin Error: %s" % child.before)

    return True
