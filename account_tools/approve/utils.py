from pexpect import spawn, ExceptionPexpect
from django.conf import settings


def run_approve(real_name, university_id, account_name, email_address, forward_mail, password):
    """Run the approve program, raising Exception for each error"""
    # university_id is generally calnet_uid
    timeout_sec = 3
    try:
        child = spawn(settings.APPROVE_BIN)

        child.expect("The authenticity", timeout=timeout_sec)
        child.sendline("yes")

        child.expect("Is this", timeout=timeout_sec)
        child.sendline("i")
    except ExceptionPexpect:
        raise Exception("Could not run approval program.")

    try:
        child.expect("Real name", timeout=timeout_sec)
        child.sendline(real_name)
    except ExceptionPexpect:
        raise Exception("Could not run approval program.")

    try:
        child.expect("University ID", timeout=timeout_sec)
        child.sendline(university_id)
    except ExceptionPexpect:
        raise Exception("Error submitting name.")

    try:
        child.expect("Requested account name", timeout=timeout_sec)
        child.sendline(account_name)
    except ExceptionPexpect:
        raise Exception("Error submitting ID.")

    try:
        child.expect("Enter your email address", timeout=timeout_sec)
        child.sendline(email_address)
    except ExceptionPexpect:
        if "Duplicate username found in approved users file" in child.before:
            raise Exception("There is a duplicate account name awaiting approval.")
        elif "This account name has already been taken" in child.before:
            raise Exception("This account name has already been taken.")
        else:
            raise Exception("Error submitting account name.")

    try:
        child.expect("Enter again to confirm", timeout=timeout_sec)
        child.sendline(email_address)
    except ExceptionPexpect:
        raise Exception("Error submitting email address.")

    try:
        child.expect("Your OCF account", timeout=timeout_sec)
        if forward_mail:
            child.sendline("y")
        else:
            child.sendline("n")
    except ExceptionPexpect:
        raise Exception("Error confirming email address.")

    # Shifting errors by one
    try:
        child.expect("Choose a password", timeout=timeout_sec)
        child.sendline(password)
        child.expect("Enter again to verify", timeout=timeout_sec)
        child.sendline(password)
    except ExceptionPexpect:
        raise Exception("Weak password rejected.")

    try:
        child.expect("The account has been approved successfully", timeout=timeout_sec)
    except ExceptionPexpect:
        raise Exception("Error approving account.")

    return True
