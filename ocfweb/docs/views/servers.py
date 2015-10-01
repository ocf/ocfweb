from django.shortcuts import render_to_response
from django.template import RequestContext


def servers(doc, request):
    return render_to_response(
        'servers.html',
        {
            'title': 'Servers',
        },
        context_instance=RequestContext(request),
    )
