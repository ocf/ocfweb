import base64
import os
import pexpect
import socket
import time

from django.conf import settings
from ocf.utils import clean_user_account, clean_password


def _kadmin_command(user_account):
    user_account = clean_user_account(user_account)
    return "%(kadmin_location)s -K %(kerberos_keytab)s -p %(kerberos_principal)s cpw %(user_account)s" % {
            "kadmin_location": settings.KADMIN_LOCATION,
            "kerberos_keytab": settings.KRB_KEYTAB,
            "kerberos_principal": "chpass/" + socket.getfqdn(),
            "user_account": user_account
        }


def change_krb_password(user_account, new_password):
    """Change a user's Kerberos password.

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

    child.expect("Verify password - %s@OCF.BERKELEY.EDU's Password:" % user_account)
    child.sendline(new_password)

    child.expect(pexpect.EOF)
    if "kadmin" in child.before:
        raise Exception("kadmin Error: %s" % child.before)

    return True
