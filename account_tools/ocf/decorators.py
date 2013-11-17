from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.core.urlresolvers import reverse


def https_required(function=None):
    def _decorator(request, *args, **kwargs):
        if not request.is_secure():
            return HttpResponsePermanentRedirect("https://%s/%s" % \
                (request.get_host(), request.get_full_path()))
        return function(request, *args, **kwargs)
    return _decorator

def login_required(function):
    def _decorator(request, *args, **kwargs):
        if "ocf_user" in request.session:
            return function(request, *args, **kwargs)
        
        request.session["login_return_path"] = request.get_full_path()
        return HttpResponseRedirect(reverse("login"))

    return _decorator
