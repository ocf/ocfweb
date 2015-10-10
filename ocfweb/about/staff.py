from django.shortcuts import render_to_response
from django.template import RequestContext


def about_staff(request):
    return render_to_response(
        'staff.html',
        {
            'title': 'Join the Staff Team',
        },
        context_instance=RequestContext(request),
    )
