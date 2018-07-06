from django.http import HttpResponse

SECURITY_TXT = """\
OpenBugBounty: https://openbugbounty.org/bugbounty/ucbocf/
"""


def openbugbounty_security(request):
    """Serve the OpenBugBounty security.txt file."""

    return HttpResponse(SECURITY_TXT, content_type='text/plain')
