from urllib.parse import urlencode

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


def login_required(fn):
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
