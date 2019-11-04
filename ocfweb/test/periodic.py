from operator import attrgetter
from typing import Any

from django.http import HttpResponse
from django.shortcuts import render

from ocfweb.caching import periodic_functions


def test_list_periodic_functions(request: Any) -> HttpResponse:
    return render(
        request,
        'test/periodic.html',
        {
            'title': 'Periodic Functions List',
            'periodic_functions': sorted(periodic_functions, key=attrgetter('function_call_key')),
        },
    )
