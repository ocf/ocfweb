"""Introspection into the current environment."""
import os
from functools import lru_cache


@lru_cache
def ocfweb_version() -> str:
    """Return string representing ocfweb version.

    In dev, returns 'dev'. In prod, returns a version
    similar to '2019-08-20-T21-10-57-gite0ca5b9'.
    """
    # On Kubernetes, read it out of environ
    try:
        return os.environ['OCFWEB_PROD_VERSION']
    except KeyError:
        pass

    # Otherwise, we must be in dev.
    return 'dev'
