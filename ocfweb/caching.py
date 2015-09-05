"""Caching decorators for ocfweb.

Provides the following decorators:

    @lru_cache(...)
    Arguments:
        - maxsize (default: 1024)
        - typed (default: True)

    @ttl_cache(...)
    Arguments:
        - ttl (in seconds; default: 60)
        - maxsize (default: 1024)
        - typed (default: True)
"""
from functools import partial

import cachetools.func


def _make_decorator(decorator, **kwargs):
    def real_decorator(fn):
        return decorator(**kwargs)(fn)
    return real_decorator


lru_cache = partial(
    _make_decorator,
    cachetools.func.lru_cache,
    maxsize=1024,
    typed=True,
)

ttl_cache = partial(
    _make_decorator,
    cachetools.func.ttl_cache,
    ttl=60,
    maxsize=1024,
    typed=True,
)
