#!/usr/bin/env python3
"""Run periodic functions.

This runs all periodic functions, either in a looping mode designed to run
forever in the background (default), or in a "single-run" mode (pass `-s`)
useful in development.
"""
import logging
import os
import time
from argparse import ArgumentParser
from textwrap import dedent
from traceback import format_exc

from django.conf import settings
from ocflib.misc.mail import send_problem_report
from ocflib.misc.shell import bold
from ocflib.misc.shell import green
from ocflib.misc.shell import yellow

from ocfweb.caching import periodic_functions


_logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# seconds to pause worker after encountering an error
DELAY_ON_ERROR_MIN = 30
DELAY_ON_ERROR_MAX = 1800  # 30 minutes
delay_on_error = DELAY_ON_ERROR_MIN


def run_periodic_functions():
    global delay_on_error

    # First, import urls so that views are imported, decorators are run, and
    # our periodic functions get registered.
    import ocfweb.urls  # noqa

    was_error = False

    for pf in periodic_functions:
        if pf.seconds_since_last_update() >= pf.period:
            _logger.info(bold(green('Updating periodic function: {}'.format(pf))))

            try:
                pf.update()
            except Exception as ex:
                was_error = True
                if isinstance(ex, KeyboardInterrupt) or settings.DEBUG:
                    raise

                try:
                    send_problem_report(dedent(
                        """\
                        An exception occured in an ocfweb periodic function:

                        {traceback}

                        Periodic function:
                          * Key: {pf.function_call_key}
                          * Last Update: {last_update} ({seconds_since_last_update} seconds ago)
                          * Period: {pf.period}
                          * TTL: {pf.ttl}

                        The background process will now pause for {delay} seconds.
                        """
                    ).format(
                        traceback=format_exc(),
                        pf=pf,
                        last_update=pf.last_update(),
                        seconds_since_last_update=pf.seconds_since_last_update(),
                        delay=delay_on_error,
                    ))
                    _logger.error(format_exc())
                except Exception as ex:
                    print(ex)  # just in case it errors again here
                    send_problem_report(dedent(
                        """\
                        An exception occured in ocfweb, but we errored trying to report it:

                        {traceback}
                        """
                    ).format(traceback=format_exc()))
                    raise

        else:
            _logger.debug(bold(yellow('Not updating periodic function: {}'.format(pf))))

    if was_error:
        delay_on_error = min(DELAY_ON_ERROR_MAX, delay_on_error * 2)
        time.sleep(delay_on_error)
    else:
        delay_on_error = max(DELAY_ON_ERROR_MIN, delay_on_error / 2)


def main(argv=None):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'ocfweb.settings'

    parser = ArgumentParser(description='Run ocfweb periodic functions')
    parser.add_argument(
        '-s',
        '--single-run',
        help='Run periodic functions once and then quit (default is to run forever).',
        action='store_true',
        default=False,
    )
    args = parser.parse_args(argv)

    if args.single_run:
        _logger.info('Running periodic functions once.')
        run_periodic_functions()
    else:
        _logger.info('Running periodic functions repeatedly.')
        while True:
            run_periodic_functions()
            time.sleep(1)


if __name__ == '__main__':
    exit(main())
