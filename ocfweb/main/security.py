from typing import Any

from django.http import HttpResponse

SECURITY_TXT = """\
Contact: mailto:security@ocf.berkeley.edu
OpenBugBounty: https://openbugbounty.org/bugbounty/ucbocf/
"""


def security_dot_txt(request: Any) -> HttpResponse:
    """Serve the security.txt file."""
    return HttpResponse(SECURITY_TXT, content_type='text/plain')
