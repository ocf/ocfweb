"""Introspection into the current environment."""
from functools import lru_cache

import pkg_resources


@lru_cache()
def ocfweb_version():
    """Return string representing ocfweb version.

    In dev, returns 'dev'. In prod, returns a version
    similar to '2015.12.06.02.25-gitb98c8cb6'.
    """
    try:
        return pkg_resources.get_distribution('ocfweb').version
    except pkg_resources.DistributionNotFound:
        # in dev, the ocfweb package isn't actually installed via setuptools
        return 'dev'
