"""Introspection into the current environment."""
import os
from functools import lru_cache


@lru_cache()
def ocfweb_version():
    """Return string representing ocfweb version.

    In dev, returns 'dev'. In prod, returns a version
    similar to '2015.12.06.02.25-gitb98c8cb6'.
    """
    # On Marathon, read it out of environ
    try:
        docker_image, tag = os.environ['MARATHON_APP_DOCKER_IMAGE'].split(':', 1)
        return tag
    except KeyError:
        pass

    # Otherwise, we must be in dev.
    return 'dev'
