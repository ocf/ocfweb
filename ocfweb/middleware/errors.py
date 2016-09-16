from pprint import pformat
from textwrap import dedent
from traceback import format_exc

from django.conf import settings
from django.http.response import Http404
from ocflib.misc.mail import send_problem_report

from ocfweb.component.errors import ResponseException


class OcflibErrorMiddleware:

    def process_exception(self, request, exception):
        if isinstance(exception, ResponseException):
            return exception.response

        # maybe it's a real exception?
        if settings.DEBUG or settings.TESTING:
            return

        if isinstance(exception, Http404):
            # we don't care about reporting 404 errors
            return

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
                traceback=format_exc(),
                request=request,
                host=request.get_host(),
                path=request.get_full_path(),
                is_secure=request.is_secure(),
                session=pformat(dict(request.session)),
                headers=pformat(request.META),
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
