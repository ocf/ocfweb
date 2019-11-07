from os import getpid

from django.http import HttpRequest
from django.http import HttpResponse


def test_session(request: HttpRequest) -> HttpResponse:
    request.session.setdefault('n', 0)
    request.session['n'] += 1
    return HttpResponse('pid={} n={}'.format(getpid(), request.session['n']))
