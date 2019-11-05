from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render


def about_staff(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        'about/staff.html',
        {
            'title': 'Join the Staff Team',
        },
    )
