from operator import attrgetter

from django.shortcuts import render

from ocfweb.caching import periodic_functions


def test_list_periodic_functions(request):
    return render(
        request,
        'test/periodic.html',
        {
            'title': 'Periodic Functions List',
            'periodic_functions': sorted(periodic_functions, key=attrgetter('function_call_key')),
        },
    )
