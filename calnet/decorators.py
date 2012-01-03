try:
    from functools import update_wrapper, wraps
except ImportError:
    from django.utils.functional import update_wrapper, wraps  # Python 2.4 fallback.

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import HttpResponseRedirect
from django.utils.decorators import available_attrs
from django.utils.http import urlquote

def session_passes_test(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    if not login_url:
        from django.conf import settings
        login_url = settings.LOGIN_URL

    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request):
                return view_func(request, *args, **kwargs)
            path = urlquote(request.META.get('HTTP_REFERER', request.get_full_path()))
            tup = login_url, redirect_field_name, path
            return HttpResponseRedirect('%s?%s=%s' % tup)
        return wraps(view_func, assigned=available_attrs(view_func))(_wrapped_view)
    return decorator


def login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """Decorator for views.
    If the session doesn't have a non-None calnet_uid value, redirects to CalNet login view
    """
    actual_decorator = session_passes_test(
        lambda request: "calnet_uid" in request.session and request.session["calnet_uid"],
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

