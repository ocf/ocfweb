from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.core.urlresolvers import reverse
from ocf.utils import user_is_group
from django.conf import settings

def login_required(function):
    def _decorator(request, *args, **kwargs):
        if "ocf_user" in request.session:
            return function(request, *args, **kwargs)

        request.session["login_return_path"] = request.get_full_path()
        return HttpResponseRedirect(reverse("login"))

    return _decorator

def group_account_required(function):
    def _decorator(request, *args, **kwargs):
        if user_is_group(request.session["ocf_user"]):
            return function(request, *args, **kwargs)

        return HttpResponseRedirect(reverse("group_accounts_only"))

    return _decorator
