from textwrap import dedent
from typing import Any

from django.conf import settings
from django.http import HttpResponse


def robots_dot_txt(request: Any) -> HttpResponse:
    """Serve /robots.txt file."""
    if settings.DEBUG:
        resp = """\
            User-Agent: *
            Disallow: /
        """
    else:
        resp = """\
            User-Agent: *
            Disallow: /login/calnet/
            Disallow: /test/
            Disallow: /tv/
            Disallow: /api/
        """

    return HttpResponse(
        dedent(resp),
        content_type='text/plain',
    )
