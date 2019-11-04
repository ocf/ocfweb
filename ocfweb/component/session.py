from typing import Any

from ocflib.account.validators import user_exists


def is_logged_in(request: Any) -> bool:
    """Return whether a user is logged in."""
    return bool(logged_in_user(request))


def logged_in_user(request: Any) -> str:
    """Return logged in user, or raise KeyError."""
    return request.session.get('ocf_user')


def login(request: Any, user: str) -> None:
    """Log in a user. Doesn't do any kind of password validation (obviously)."""
    assert user_exists(user)
    request.session['ocf_user'] = user


def logout(request: Any) -> bool:
    """Log out the user. Return True if a user was logged out, False otherwise."""
    try:
        del request.session['ocf_user']
    except KeyError:
        return False
    else:
        return True
