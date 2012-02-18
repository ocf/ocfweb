from django.http import get_host, HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from calnet.utils import verify_ticket
from urlparse import urljoin
from urllib import urlencode

def _service_url(request, next_page):
    protocol = ('http://', 'https://')[request.is_secure()]
    host = get_host(request)
    service = protocol + host + request.path
    url = service
    if next_page:
	    url += "?" + urlencode({REDIRECT_FIELD_NAME: next_page})
    return url


def _redirect_url(request):
    """ Redirects to referring page """
    next_page = request.META.get('HTTP_REFERER')
    prefix = ('http://', 'https://')[request.is_secure()] + get_host(request)
    if next_page and next_page.startswith(prefix):
        next_page = next_page[len(prefix):]
    return next_page

def _login_url(service):
        params = {"service": service,
                    "renew": "true"}
        return "%s?%s" % (urljoin(settings.CALNET_SERVER_URL, "login"), urlencode(params))

def _logout_url(request, next_page=None):
    url = urljoin(settings.CALNET_SERVER_URL, 'logout')
    if next_page:
        protocol = ('http://', 'https://')[request.is_secure()]
        host = get_host(request)
        url += '?' + urlencode({'url': protocol + host + next_page})
    return url

def _next_page_response(next_page):
    if next_page:
        return HttpResponseRedirect(next_page)
    else:
        return HttpResponse("<h1>Operation Successful</h1><p>Congratulations.</p>")

def login(request, next_page=None):
    next_page = request.GET.get(REDIRECT_FIELD_NAME)
    if not next_page:
        next_page = _redirect_url(request)
    if "calnet_uid" in request.session and request.session["calnet_uid"]:
        return _next_page_response(next_page)
    ticket = request.GET.get("ticket")
    service = _service_url(request, next_page)
    if ticket:
        verified_uid = verify_ticket(ticket, service)
        if verified_uid:
            request.session["calnet_uid"] = verified_uid
        if request.session.has_key("calnet_uid") and request.session["calnet_uid"]:
            return _next_page_response(next_page)
        else:
            error = "<h1>Forbidden</h1><p>CalNet login failed.</p>"
            return HttpResponseForbidden(error)
    return render_to_response("redirecting_to_calnet.html",{
        "calnet_url": _login_url(service)
    })

def logout(request, next_page=None):
    if "calnet_uid" in request.session:
        del request.session["calnet_uid"]
    if not next_page:
        next_page = getattr(settings, "CALNET_AFTER_LOGOUT_URL", None)

    if not next_page:
        next_page = _redirect_url(request)
    return HttpResponseRedirect(_logout_url(request, next_page))
