from django.shortcuts import render_to_response
from django.template import RequestContext


def home(request):
    return render_to_response(
        'home.html',
        {
            'fulltitle': 'Open Computing Facility at UC Berkeley',
            'description': (
                'The Open Computing Facility is an all-volunteer student '
                'organization dedicated to free and open-source computing for all UC '
                'Berkeley students.'''
            ),
        },
        context_instance=RequestContext(request),
    )
