from operator import attrgetter

from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render

from ocfweb.caching import periodic_functions


def test_list_periodic_functions(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        'test/periodic.html',
        {
            'title': 'Periodic Functions List',
            'periodic_functions': sorted(periodic_functions, key=attrgetter('function_call_key')),
        },
    )
