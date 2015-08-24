from django.shortcuts import render_to_response
from django.template import RequestContext
from ocflib.lab.staff_hours import get_staff_hours


def staff_hours(request):
    return render_to_response(
        'staff-hours.html',
        {
            'title': 'Staff Hours',
            'staff_hours': get_staff_hours(),
        },
        context_instance=RequestContext(request),
    )
