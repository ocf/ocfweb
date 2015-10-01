from django.shortcuts import render_to_response
from django.template import RequestContext


def docs_index(request):
    return render_to_response(
        'index.html',
        {
            'title': 'Documentation',
        },
        context_instance=RequestContext(request),
    )
