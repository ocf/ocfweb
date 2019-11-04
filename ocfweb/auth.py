# TODO: move this file into ocfweb.component.session?
from typing import Any
from typing import Callable
from typing import Optional
from urllib.parse import urlencode

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from ocflib.account.search import user_is_group

from ocfweb.component.session import is_logged_in
from ocfweb.component.session import logged_in_user


def login_required(function: Callable[..., Any]) -> Callable[..., Any]:
    def _decorator(request: Any, *args: Any, **kwargs: Any) -> Any:
        if is_logged_in(request):
            return function(request, *args, **kwargs)

        request.session['login_return_path'] = request.get_full_path()
        return HttpResponseRedirect(reverse('login'))

    return _decorator


def group_account_required(function: Callable[..., Any]) -> Callable[..., Any]:
    def _decorator(request: Any, *args: Any, **kwargs: Any) -> Any:
        try:
            user: Optional[str] = logged_in_user(request)
        except KeyError:
            user = None

        if user and user_is_group(logged_in_user(request)):
            return function(request, *args, **kwargs)

        return render(
            request, 'group_accounts_only.html', {
                'user': user,
            }, status=403,
        )

    return _decorator


def calnet_required(fn: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator for views that require CalNet auth

    Checks if "calnet_uid" is in the request.session dictionary. If the value
    is not a valid uid, the user is rediected to CalNet login view.
    """
    def wrapper(request: Any, *args: Any, **kwargs: Any) -> Any:
        calnet_uid = request.session.get('calnet_uid')
        if calnet_uid:
            return fn(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(
                '{calnet_login}?{params}'.format(
                    calnet_login=reverse('calnet_login'),
                    params=urlencode({REDIRECT_FIELD_NAME: request.get_full_path()}),
                ),
            )

    return wrapper
