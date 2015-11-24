from django.shortcuts import render_to_response
from django.template import RequestContext


def move_to_mlk(request):
    1 / 0
    return render_to_response(
        'move-to-mlk.html',
        {
            'title': 'Move to MLK Student Union (Fall 2015)',
        },
        context_instance=RequestContext(request),
    )
