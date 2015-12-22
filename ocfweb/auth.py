from urllib.parse import urlencode

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from ocflib.account.search import user_is_group


def login_required(function):
    def _decorator(request, *args, **kwargs):
        if 'ocf_user' in request.session:
            return function(request, *args, **kwargs)

        request.session['login_return_path'] = request.get_full_path()
        return HttpResponseRedirect(reverse('login'))

    return _decorator


def group_account_required(function):
    def _decorator(request, *args, **kwargs):
        if user_is_group(request.session['ocf_user']):
            return function(request, *args, **kwargs)

        return render(request, 'group_accounts_only.html', {
            'user': request.session['ocf_user']
        }, status=403)

    return _decorator


def calnet_required(fn):
    """Decorator for views that require CalNet auth

    Checks if "calnet_uid" is in the request.session dictionary. If the value
    is not a valid uid, the user is rediected to CalNet login view.
    """
    def wrapper(request, *args, **kwargs):
        calnet_uid = request.session.get('calnet_uid')
        if calnet_uid:
            return fn(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('{calnet_login}?{params}'.format(
                calnet_login=reverse('calnet_login'),
                params=urlencode({REDIRECT_FIELD_NAME: request.get_full_path()}),
            ))

    return wrapper
