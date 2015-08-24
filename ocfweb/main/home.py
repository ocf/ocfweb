from django.shortcuts import render_to_response
from django.template import RequestContext
from ocflib.lab.staff_hours import get_staff_hours_soonest_first


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
            'staff_hours': get_staff_hours_soonest_first()[:2],
        },
        context_instance=RequestContext(request),
    )
