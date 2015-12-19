import logging
import os
from argparse import ArgumentParser

from ocfweb.caching import periodic_functions


_logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def run_periodic_functions(grace_period):
    # First, import urls so that views are imported, decorators are run, and
    # our periodic functions get registered.
    import ocfweb.urls  # noqa

    for pf in periodic_functions:
        if pf.seconds_since_last_update() >= pf.period - grace_period:
            pf.update()
            _logger.info('Updating periodic function: {}'.format(pf))
        else:
            _logger.info('Not updating periodic function: {}'.format(pf))


def main(argv=None):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'ocfweb.settings'

    parser = ArgumentParser(description='Run ocfweb periodic functions')
    parser.add_argument('-g', '--grace-period', type=int, default=5)
    args = parser.parse_args(argv)

    run_periodic_functions(args.grace_period)


if __name__ == '__main__':
    exit(main())
