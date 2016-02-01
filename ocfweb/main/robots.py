from textwrap import dedent

from django.conf import settings
from django.http import HttpResponse


def robots_dot_txt(request):
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
        """

    return HttpResponse(
        dedent(resp),
        content_type='text/plain',
    )

