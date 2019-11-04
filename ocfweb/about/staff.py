from typing import Any

from django.http import HttpResponse
from django.shortcuts import render


def about_staff(request: Any) -> HttpResponse:
    return render(
        request,
        'about/staff.html',
        {
            'title': 'Join the Staff Team',
        },
    )
