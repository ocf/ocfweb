from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render


def docs_index(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        'docs/index.html',
        {
            'title': 'Documentation',
        },
    )
