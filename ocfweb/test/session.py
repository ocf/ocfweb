from os import getpid
from typing import Any

from django.http import HttpResponse


def test_session(request: Any) -> HttpResponse:
    request.session.setdefault('n', 0)
    request.session['n'] += 1
    return HttpResponse('pid={} n={}'.format(getpid(), request.session['n']))
