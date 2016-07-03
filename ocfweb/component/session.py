from ocflib.account.validators import user_exists


def is_logged_in(request):
    """Return whether a user is logged in."""
    return bool(logged_in_user(request))


def logged_in_user(request):
    """Return logged in user, or raise KeyError."""
    return request.session.get('ocf_user')


def login(request, user):
    """Log in a user. Doesn't do any kind of password validation (obviously)."""
    assert user_exists(user)
    request.session['ocf_user'] = user


def logout(request):
    """Log out the user. Return True if a user was logged out, False otherwise."""
    try:
        del request.session['ocf_user']
    except KeyError:
        return False
    else:
        return True
