from django.http import HttpResponsePermanentRedirect

def https_required(function=None):
    def _decorator(request, *args, **kwargs):
        if not request.is_secure():
            return HttpResponsePermanentRedirect("https://%s/%s" % \
                (request.get_host(), request.get_full_path()))
        return function(request, *args, **kwargs)
    return _decorator
