import re
from pprint import pformat
from textwrap import dedent
from traceback import format_exc

from django.conf import settings
from django.http.response import Http404
from ocflib.misc.mail import send_problem_report

from ocfweb.component.errors import ResponseException


SENSITIVE_WSGI_CONTEXT = frozenset((
    'HTTP_COOKIE',
    'CSRF_COOKIE',
))


def sanitize(msg):
    """Attempt to sanitize out known-bad patterns."""
    # Remove any dictionary references with "encrypted_password", e.g. lines like:
    #   {'some_key': ..., 'encrypted_password': b'asdf', 'some_other_key': ...}
    msg = re.sub(r"('encrypted_password': b?').+?('(?:,|}))", r'\1<REDACTED>\2', msg)
    return msg


def sanitize_wsgi_context(headers):
    """Attempt to sanitize out known-bad WSGI context keys."""
    headers = dict(headers)
    for key in SENSITIVE_WSGI_CONTEXT:
        if key in headers:
            headers[key] = '<REDACTED>'
    return headers


class OcflibErrorMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        if isinstance(exception, ResponseException):
            return exception.response

        # maybe it's a real exception?
        if settings.DEBUG or settings.TESTING:
            return

        if isinstance(exception, Http404):
            # we don't care about reporting 404 errors
            return

        traceback = sanitize(format_exc())
        headers = sanitize_wsgi_context(request.META)

        try:
            send_problem_report(dedent(
                """\
                An exception occured in ocfweb:

                {traceback}


                Request:
                  * Host: {host}
                  * Path: {path}
                  * Method: {request.method}
                  * Secure: {is_secure}

                Request Headers:
                {headers}

                Session:
                {session}
                """
            ).format(
                traceback=traceback,
                request=request,
                host=request.get_host(),
                path=request.get_full_path(),
                is_secure=request.is_secure(),
                session=pformat(dict(request.session)),
                headers=pformat(headers),
            ))
        except Exception as ex:
            print(ex)  # just in case it errors again here
            send_problem_report(dedent(
                """\
                An exception occured in ocfweb, but we errored trying to report it:

                {traceback}
                """
            ).format(traceback=format_exc()))
            raise
