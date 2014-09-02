from django.conf import settings
import os
import base64
import fcntl
import paramiko
from difflib import SequenceMatcher
from getpass import getuser, getpass
from pwd import getpwnam
from socket import gethostname
from time import asctime
from ocf.utils import check_email

# Dependencies
# pycrypto, cracklib, dnspython
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from cracklib import FascistCheck

class ApprovalError(Exception):
    pass

def filter_real_name(name):
    return filter(_valid_real_name_char, name)

def _valid_real_name_char(char):
    return char in " -.'" or char.isalpha()

def _check_real_name(real_name):
    if not all(map(_valid_real_name_char, real_name)):
        raise ApprovalError("Invalid characters in name: {0}".format(real_name))

def _check_university_uid(university_uid):
    try:
        int(university_uid)
    except ValueError:
        raise ApprovalError("Invalid UID number: {0}".format(university_uid))

def _check_username(username):

    # Is this a valid username?
    if len(username) > 8 or len(username) < 3:
        raise ApprovalError("Username must be between 3 and 8 letters: {0}".format(username))
    elif any([not i.islower() for i in username]):
        raise ApprovalError("Username must contain only lowercase letters: {0}".format(username))

    # Is the username already taken?
    try:
        getpwnam(username)
        raise ApprovalError("Username already in use: {0}".format(username))
    except KeyError:
        pass

    # Is the username already requested?
    try:
        with open(settings.APPROVE_FILE) as f:
            for line in f:
                if line.startswith(username + ":"):
                    raise ApprovalError("Username already requested: {0}".format(username))
    except IOError:
        pass

    # Is the username reserved?
    with open(settings.OCF_RESERVED_NAMES_LIST) as reserved:
        for line in reserved:
            if line.strip() == username:
                raise ApprovalError("Username is reserved: {0}".format(username))

def _string_match_percentage(a, b):
    return sum([i.lower() == j.lower()
                for index in range(len(a))
                for i, j in zip(a[index:], b)]) / float(len(a))

def _check_password(password, username):
    if len(password) < 8:
        raise ApprovalError("Password must be at least 8 characters")

    s = SequenceMatcher()
    s.set_seqs(password, username)
    threshold = 0.6
    if s.ratio() > threshold:
        raise ApprovalError("Password is too similar to username")

    # XXX: Double quotes are exploitable when adding through kadmin
    if "\n" in password or "\r" in password:
        raise ApprovalError("Newlines and carriage returns are forbidden in passwords")

    if FascistCheck:
        try:
            FascistCheck(password)
        except ValueError as e:
            raise ApprovalError("Password problem: {0}".format(e))

def _check_email(email):
    if not check_email(email):
        raise ApprovalError("Invalid email address: {0}".format(email))

def _encrypt_password(password):
    # Use an asymmetric encryption algorithm to allow the keys to be stored on disk
    # Generate the public / private keys with the following code:
    # >>> from Crypto.PublicKey import RSA
    # >>> key = RSA.generate(2048)
    # >>> open("private.pem", "w").write(key.exportKey())
    # >>> open("public.pem", "w").write(key.publickey().exportKey())

    key = RSA.importKey(open(settings.PASSWORD_PUB_KEY).read())
    RSA_CIPHER = PKCS1_OAEP.new(key)
    return RSA_CIPHER.encrypt(password)

def approve_user(real_name, calnet_uid, account_name, email, password):
    _check_real_name(real_name)
    _check_university_uid(calnet_uid)
    _check_username(account_name)
    _check_email(email)
    _check_password(password, real_name)

    _approve(calnet_uid, email, account_name, password, real_name = real_name)

def _approve(university_uid, email, account_name, password, real_name = None,
        responsible = None):

    group_name = "(null)"
    group = 0
    responsible = "(null)"

    # Encrypt the password and base64 encode it
    password = base64.b64encode(_encrypt_password(password.encode()))

    # Write to the list of users to be approved
    sections = [account_name, real_name, group_name,
                email, 0, group, password,
                university_uid, responsible]

    with open(settings.APPROVE_FILE, "a") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write(":".join([str(i) for i in sections]) + "\n")
        fcntl.flock(f, fcntl.LOCK_UN)

    # Write to the log
    name = real_name

    sections = [account_name, name, university_uid,
                email, getuser(), gethostname(),
                0, group, asctime(), responsible]

    with open(settings.APPROVE_LOG, "a") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write(":".join([str(i) for i in sections]) + "\n")
        fcntl.flock(f, fcntl.LOCK_UN)

    _trigger_create()

def _trigger_create():
    """Attempt to trigger a create run."""
    key = paramiko.RSAKey.from_private_key_file(settings.ADMIN_SSH_KEY)
    ssh = paramiko.SSHClient()
    ssh.load_host_keys(settings.CMDS_HOST_KEYS_FILENAME)
    ssh.connect(hostname='admin.ocf.berkeley.edu', username='atool', pkey=key)
    ssh.exec_command('/srv/atool/bin/create')
