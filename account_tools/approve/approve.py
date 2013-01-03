from django.conf import settings
import os
import base64
from getpass import getuser, getpass
from socket import gethostname
from time import asctime

# Dependencies
from cracklib import FascistCheck

class ApprovalError(Exception):
    pass

def _check_real_name(real_name):
    if not all([i == " " or i.isalpha() for i in real_name]):
        raise ApprovalError("The only permitted characters are uppercase, "
                        "lowercase, and spaces")

def _check_calnet_uid(calnet_uid):
    if not all([i.isdigit() for i in calnet_uid]):
        raise ApprovalError("This doesn't appear to be a valid calnet uid")

def _check_username(username):
    if len(username) > 8 or len(username) < 3:
        raise ApprovalError("Usernames must be between 3 and 8 characters")
    elif any([not i.islower() for i in username]):
        raise ApprovalError("Usernames must consist of only lowercase alphabet")

    # In approved user file
    try:
        with open(settings.ACCOUNT_FILE) as f:
            for line in f:
                if line.startswith(username + ":"):
                    raise ApprovalError("Duplicate username found in approved users file")
    except IOError:
        pass

    with open(settings.OCF_RESERVED_NAMES_LIST) as reserved:
        for line in reserved:
            if line.strip() == username:
                raise ApprovalError("Username is reserved")

def _check_forward(forward):
    if forward not in ["y", "n"]:
        raise ApprovalError("Please only type in a lowercase y or a lowercase n")

def _string_match_percentage(a, b):
    return sum([i.lower() == j.lower()
                for index in range(len(a))
                for i, j in zip(a[index:], b)]) / float(len(a))

def _check_password(password, username):
    if len(password) < 8:
        raise ApprovalError("The password you entered is too short (minimum of 8 chars)")

    percentage = _string_match_percentage(password, username)
    # Threshold?

    try:
        FascistCheck(password)
    except ValueError as e:
        raise ApprovalError("Password issue: {}".format(e))

def _check_email(email):
    if email.find("@") == -1 or email.find(".") == -1:
        raise ApprovalError("Invalid Entry, it doesn't look like an email")

def approve_user(real_name, calnet_uid, account_name, email, password,
                 forward = False):
    _check_real_name(real_name)
    _check_university_id(calnet_uid)
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

def _approve(calnet_uid, email, account_name, password, forward = False,
             real_name = "(null)", group_name = "(null)", responsible = None):
    if group_name:
        group = 1
        real_name = "(null)"
    else:
        group_name = "(null)"
        group = 0

    forward = int(bool(forward))
    password = base64.b64encode(password)

    # Write to the list of users to be approved
    sections = (username, real_name, group_name,
                email, forward, group, password, " ",
                university_id)

    with FileLock(settings.ACCOUNT_FILE):
        with open(settings.ACCOUNT_FILE, "a") as f:
            f.write(":".join((str(i) for i in sections)) + "\n")

    # Write to the log
    sections = [username, responsible, university_id,
                getuser(), gethostname(),
                1 if os.geteuid() == os.getuid() else 0,
                1 if group_name else 0, asctime()]

    with open(settings.ACCOUNT_LOG, "a") as f:
        f.write(":".join((str(i) for i in sections)) + "\n")
