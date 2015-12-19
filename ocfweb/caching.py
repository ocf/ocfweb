"""Caching decorators for ocfweb."""
from itertools import chain

from django.conf import settings
from django.core.cache import cache as django_cache

from ocfweb.environment import ocfweb_version


def cache_lookup_with_fallback(key, fallback, ttl=None, force_miss=False):
    """Look up a key in the cache, falling back to a function if it's a miss.

    We first check if the key is in the cache, and if so, return it. If not, we
    evaluate the fallback function, stick the result in the cache for next
    time, and then return the result.

    In DEBUG mode, we still retrieve and store from the cache (in order to
    exercise as much of the code as possible), but we always force a miss.

    :param key: the key to look up
    :param fallback: a function to evaluate if we get a cache miss;
                     the result will be inserted into the cache for next time
    :param ttl: the ttl to use (optional, if not specified, keys never expire)
    :param force_miss: whether to force a cache miss (and thus evaluate the
                       fallback and store it in the cache)
    """
    # The "get" method returns `None` both for cached values of `None`,
    # and keys which aren't in the cache.
    #
    # The recommended workaround is using a sentinel as a default
    # return value for when a key is missing. This allows us to still
    # cache functions which return None.
    cache_miss_sentinel = {}
    retval = django_cache.get(key, cache_miss_sentinel)
    is_hit = retval is not cache_miss_sentinel

    if is_hit and not settings.DEBUG and not force_miss:
        # cache hit
        return retval
    else:
        # cache miss
        result = fallback()
        django_cache.set(key, result, ttl)
        return result


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
        def inner(*args, **kwargs):
            return cache_lookup_with_fallback(
                _make_function_call_key(fn, args, kwargs),
                lambda: fn(*args, **kwargs),
                ttl=ttl,
            )
        return inner
    return outer


def _make_key(key):
    """Return a key suitable for caching.

    The returned key prepends a version tag so that we don't share the cache
    across ocfweb versions. This prevents strange behavior (e.g. if you change
    the return type of a function which was cached on the previous version).

    :param key: some iterable key (e.g. a tuple or list)
    """
    return tuple(chain(
        [ocfweb_version()],
        key,
    ))


def _make_function_call_key(fn, args, kwargs):
    """Return a key for a function call.

    The key will eventually be converted to a string and used as a cache key.
    We attempt to make it resistant to obvious ordering issues.

    :param fn: function
    :param args: tuple or list of arguments
    :param kwargs: dict of keyword arguments
    """
    return _make_key((
        '{fn.__module__}#{fn.__name__}'.format(fn=fn),
        tuple(args),
        tuple((k, v) for k, v in sorted(kwargs.items())),
    ))
