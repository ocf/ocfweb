from operator import attrgetter

from django.shortcuts import render_to_response
from django.template import RequestContext

from ocfweb.caching import periodic_functions


def test_list_periodic_functions(request):
    return render_to_response(
        'periodic.html',
        {
            'title': 'Periodic Functions List',
            'periodic_functions': sorted(periodic_functions, key=attrgetter('function_call_key')),
        },
        context_instance=RequestContext(request),
    )
