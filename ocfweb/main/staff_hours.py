import time

from django.shortcuts import render_to_response
from django.template import RequestContext
from ocflib.lab.staff_hours import get_staff_hours

from ocfweb.component.lab_status import get_lab_status


def staff_hours(request):
    return render_to_response(
        'staff-hours.html',
        {
            'title': 'Staff Hours',
            'staff_hours': get_staff_hours(),
            'today': time.strftime('%A'),
            'lab_status': get_lab_status(),
        },
        context_instance=RequestContext(request),
    )
