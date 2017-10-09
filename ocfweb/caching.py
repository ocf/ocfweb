"""Caching decorators for ocfweb."""
import logging
import math
from collections import namedtuple
from datetime import datetime
from itertools import chain

from cached_property import cached_property
from django.conf import settings
from django.core.cache import cache as django_cache

from ocfweb.environment import ocfweb_version


_logger = logging.getLogger(__name__)


def cache_lookup(key):
    """Look up a key in the cache, raising KeyError if it's a miss."""
    # The "get" method returns `None` both for cached values of `None`,
    # and keys which aren't in the cache.
    #
    # The recommended workaround is using a sentinel as a default
    # return value for when a key is missing. This allows us to still
    # cache functions which return None.
    cache_miss_sentinel = {}
    retval = django_cache.get(key, cache_miss_sentinel)
    is_hit = retval is not cache_miss_sentinel

    if not is_hit:
        _logger.debug('Cache miss: {}'.format(key))
        raise KeyError('Key "{}" is not in the cache.'.format(key))
    else:
        _logger.debug('Cache hit: {}'.format(key))
        return retval


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
    try:
        if force_miss:
            raise KeyError('Forcing miss as requested.')

        result = cache_lookup(key)

        if settings.DEBUG:
            _logger.debug('Cache hit for "{}", but forcing miss due to DEBUG.'.format(key))
            raise KeyError('Forcing miss due to DEBUG mode.')

        return result
    except KeyError:
        result = fallback()
        django_cache.set(key, result, ttl)
        return result


def cache(ttl=None):
    """Caching function decorator, with an optional ttl.

    The optional ttl (in seconds) specifies how long cache entries should live.
    If not specified, cache entries last until the site rolls.

    If you find yourself using the TTL for anything other than to control the
    cache size (e.g. because your entries become stale), consider using the
    @periodic decorator below instead.

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


periodic_functions = set()


class PeriodicFunction(namedtuple(
    'PeriodicFunction', [
        'function',
        'period',
        'ttl',
    ],
)):

    def __hash__(self):
        return hash(self.function_call_key)

    def __eq__(self, other):
        return self.function_call_key == other.function_call_key

    def __str__(self):
        return 'PeriodicFunction({})'.format(self.function_call_key)

    @cached_property
    def function_call_key(self):
        """Return the function's cache key."""
        return _make_function_call_key(self.function, (), {})

    def function_with_timestamp(self):
        """Return a tuple (timestamp, result).

        This is the value we actually store in the cache; the benefit is that
        we can find the time a record was entered.

        Storing them in the same record helps to avoid race conditions.
        """
        return (datetime.now(), self.function())

    def last_update(self):
        """Return the timestamp of the last update of this function.

        If the function has never been updated, returns None."""
        try:
            timestamp, result = cache_lookup(self.function_call_key)
            return timestamp
        except KeyError:
            return None

    def seconds_since_last_update(self):
        """Return the number of seconds since the last update.

        If we've never updated, we return the number of seconds since
        1970 so that you can still do the normal type of comparisons.
        """
        last_update = self.last_update() or datetime.fromtimestamp(0)
        return (datetime.now() - last_update).total_seconds()

    def result(self, **kwargs):
        """Return the result of this periodic function.

        In most cases, we can read it from the cache and so it is nearly
        instant. If for some reason it isn't in the cache, we execute it (and
        then stick it in the cache for next time).
        """
        if kwargs:
            return self.function(**kwargs)

        timestamp, result = cache_lookup_with_fallback(
            self.function_call_key,
            self.function_with_timestamp,
            ttl=self.ttl,
        )
        return result

    def update(self):
        """Run this periodic function and cache the result."""
        cache_lookup_with_fallback(
            self.function_call_key,
            self.function_with_timestamp,
            ttl=self.ttl,
            force_miss=True,
        )


def periodic(period, ttl=None):
    """Caching function decorator for functions which desire TTL-based caching.

    Using this decorator on a function registers it as a "periodic function",
    with the given period in seconds. The function will be run in the
    background at the requested frequency.

    When the function is called normally, a recent cached verison will thus
    almost certainly be available for immediate use, making the website fast
    for all users.

    The optional ttl (in seconds) specifies how long cache entries should live.
    By default, it is twice the period. If your function is called without
    being cached, it is synchronously executed (and the result stored for next
    time), much like the @cache decorator.

    Periodic functions can have no required arguments. While they can have
    keyword arguments, no caching is done if you call the function using them.

    Uses the Django cache (which uses Redis) to achieve a shared cache across
    worker processes.

    In DEBUG mode, no caching is done.

    Usage:

        @periodic(60)
        def get_blog_posts():
            ....
    """
    if period == math.inf:
        assert ttl is None, ttl
        # In the Django cache framework, None means cache forever.
        ttl = None
    elif ttl is None:
        ttl = period * 2

    def outer(fn):
        pf = PeriodicFunction(
            function=fn,
            period=period,
            ttl=ttl,
        )
        periodic_functions.add(pf)
        return pf.result

    return outer
