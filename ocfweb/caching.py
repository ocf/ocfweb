"""Caching decorators for ocfweb."""
from django.conf import settings
from django.core.cache import cache as django_cache

from ocfweb.environment import ocfweb_version


def cache(ttl=None):
    """Caching function decorator, with an optional ttl.

    The optional ttl (in seconds) specifies how long cache entries should live.
    If not specified, cache entries last until the site rolls.

    Uses the Django cache (which uses Redis) to achieve a shared cache across
    worker processes.

    In DEBUG mode, no caching is done.

    Usage:

        @cache()
        def my_deterministic_function(a, b, c):
            ....

        @cache(ttl=60)
        def my_changing_function(a, b, c):
            ....
    """
    def outer(fn):
        if settings.DEBUG:
            return fn

        def inner(*args, **kwargs):
            key = (
                # We include the ocfweb version so that we don't use caches
                # from a previous deployment (in case redis doesn't get restarted).
                # The function may have changed since the old version, so we
                # might get inconsistent results if we use its cache.
                ocfweb_version(),
                '{fn.__module__}#{fn.__name__}'.format(fn=fn),
                args,
                tuple((k, v) for k, v in sorted(kwargs.keys())),
            )

            if key in django_cache:
                return django_cache.get(key)

            result = fn(*args, **kwargs)
            django_cache.set(key, result, ttl)
            return result

        return inner
    return outer
