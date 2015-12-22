from textwrap import dedent

from django.http import HttpResponse


def robots_dot_txt(request):
    """Serve /robots.txt file."""
    return HttpResponse(
        dedent("""\
            User-Agent: *
            Disallow: /test/
        """),
        content_type='text/plain',
    )
