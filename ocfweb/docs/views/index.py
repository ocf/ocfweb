from typing import Any

from django.http import HttpResponse
from django.shortcuts import render


def docs_index(request: Any) -> HttpResponse:
    return render(
        request,
        'docs/index.html',
        {
            'title': 'Documentation',
        },
    )
