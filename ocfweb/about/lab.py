from django.shortcuts import render_to_response
from django.template import RequestContext


def lab_open_source(request):
    return render_to_response(
        'lab-open-source.html',
        {
            'title': 'Open Source in our Computer Lab',
        },
        context_instance=RequestContext(request),
    )
