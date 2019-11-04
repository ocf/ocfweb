from os.path import dirname
from os.path import join
from typing import Any

from django.http import HttpResponse


def favicon(request: Any) -> HttpResponse:
    """favicon.ico must be served from the root for legacy reasons."""
    with open(join(dirname(dirname(__file__)), 'static', 'img', 'favicon', 'favicon.ico'), 'rb') as f:
        return HttpResponse(
            f.read(),
            content_type='image/x-icon',
        )
