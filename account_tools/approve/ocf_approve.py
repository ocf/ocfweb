from django.conf import settings
import os
import base64
from getpass import getuser, getpass
from socket import gethostname
from time import asctime
import fcntl

# Dependencies
# pycrypto + cracklib (Optional)
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

try:
    from cracklib import FascistCheck
except ImportError:
    FascistCheck = None

RSA_CIPHER = None

class ApprovalError(Exception):
    pass

def _check_real_name(real_name):
    if not all([i in " -" or i.isalpha() for i in real_name]):
        raise ApprovalError("Real name contains invalid characters")

def _check_calnet_uid(calnet_uid):
    try:
        int(calnet_uid)
    except ValueError:
        raise ApprovalError("This doesn't appear to be a valid calnet uid")

def _check_username(username):
    if len(username) > 8 or len(username) < 3:
        raise ApprovalError("Usernames must be between 3 and 8 characters")
    elif any([not i.islower() for i in username]):
        raise ApprovalError("Usernames must consist of only lowercase alphabet")

    # In approved user file
    try:
        with open(settings.APPROVE_FILE) as f:
            for line in f:
                if line.startswith(username + ":"):
                    raise ApprovalError("Duplicate username found in approved users file")
    except IOError:
        pass

    with open(settings.OCF_RESERVED_NAMES_LIST) as reserved:
        for line in reserved:
            if line.strip() == username:
                raise ApprovalError("Username is reserved")

def _string_match_percentage(a, b):
    return sum([i.lower() == j.lower()
                for index in range(len(a))
                for i, j in zip(a[index:], b)]) / float(len(a))

def _check_password(password, username):
    if len(password) < 8:
        raise ApprovalError("The password you entered is too short (minimum of 8 chars)")

    percentage = _string_match_percentage(password, username)
    # Threshold?

    # XXX: Double quotes are exploitable when adding through kadmin
    if "\"" in password or "\n" in password or "\r" in password:
        raise ApprovalError("Double quotes and newlines are forbidden in passwords")

    if FascistCheck:
        try:
            FascistCheck(password)
        except ValueError as e:
            raise ApprovalError("Password issue: {0}".format(e))

def _check_email(email):
    """
    Technically the check for a valid email is to mail to that address with a
    confirmation link, but this'll do as a quick basic check.
    """
    if email.find("@") == -1 or email.find(".") == -1:
        raise ApprovalError("Invalid Entry, it doesn't look like an email")

def _encrypt_password(password):
    # Use an asymmetric encryption algorithm to allow the keys to be stored on disk
    # Generate the public / private keys with the following code:
    # >>> from Crypto.PublicKey import RSA
    # >>> key = RSA.generate(2048)
    # >>> open("private.pem", "w").write(key.exportKey())
    # >>> open("public.pem", "w").write(key.publickey().exportKey())

    global RSA_CIPHER

    if RSA_CIPHER is None:
        key = RSA.importKey(open(settings.PASSWORD_PUB_KEY).read())
        RSA_CIPHER = PKCS1_OAEP.new(key)

    return RSA_CIPHER.encrypt(password)

def approve_user(real_name, calnet_uid, account_name, email, password,
                 forward = False):
    _check_real_name(real_name)
    _check_calnet_uid(calnet_uid)
    _check_username(account_name)
    _check_email(email)
    _check_password(password, real_name)

    _approve(calnet_uid, email, account_name, password,
             forward = forward, real_name = real_name)

def approve_group(group_name, responsible, calnet_uid, email, account_name, password,
                  forward = False):
    _check_real_name(group_name)
    _check_real_name(responsible)
    _check_calnet_uid(calnet_uid)
    _check_username(account_name)
    _check_email(email)
    _check_password(password, group_name)

    _approve(calnet_uid, email, account_name, password, forward = forward,
             group_name = group_name, responsible = responsible)

def _approve(university_uid, email, account_name, password, forward = False,
             real_name = None, group_name = None, responsible = None):
    assert (real_name is None) != (group_name is None)

    if group_name:
        group = 1
        real_name = "(null)"
    else:
        group_name = "(null)"
        group = 0

    # Encrypt the password and base64 encode it
    password = base64.b64encode(_encrypt_password(password.encode()))

    # Write to the list of users to be approved
    sections = [account_name, real_name, group_name,
                email, int(forward), group, password,
                university_uid]

    with open(settings.APPROVE_FILE, "a") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write(":".join([str(i) for i in sections]) + "\n")
        fcntl.flock(f, fcntl.LOCK_UN)

    # Write to the log
    name = group_name if group else real_name

    sections = [account_name, name, university_uid,
                email, getuser(), gethostname(),
                0, group, asctime()]

    with open(settings.APPROVE_LOG, "a") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write(":".join([str(i) for i in sections]) + "\n")
        fcntl.flock(f, fcntl.LOCK_UN)
