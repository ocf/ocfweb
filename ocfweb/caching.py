import sys
from functools import lru_cache as _lru_cache

from django.conf import settings


def lru_cache(*args, prod_only=True, **kwargs):
    """Decorator for an LRU cache which wraps functools.lru_cache.

    Compared to functools.lru_cache, it has the following benefits:
       - Usually won't cache when the Django DEBUG setting is true.
       - Falls back to omitting `typed` on Python <= 3.2
       - Slightly larger default size

    Usage:

        @lru_cache
        def expensive_function():
            ....

        @lru_cache(prod_only=False, maxsize=128)
        def expensive_function():
            ....
    """
    def real_decorator(fn):
        kargs = dict({
            'maxsize': 1024,
            'typed': True,
        }, **kwargs)
        if sys.version_info < (3, 3):
            del kargs['typed']

        if settings.DEBUG and prod_only:
            return fn

        return _lru_cache(**kargs)(fn)

    if len(args) == 1 and not kwargs:
        # allow using as @lru_cache (with no arguments and without calling)
        fn, = args
        return real_decorator(fn)

    return real_decorator
