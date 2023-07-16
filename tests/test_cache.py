from functools import _lru_cache_wrapper

import ee

import eerepr
from eerepr.repr import _get_cached_repr


def test_disabled_cache():
    eerepr.initialize(max_cache_size=0)
    x = ee.Number(0)
    assert not isinstance(x._ipython_display_, _lru_cache_wrapper)


def test_nondeterministic_caching():
    """ee.List.shuffle(seed=False) is nondeterministic. Make sure it misses the cache.
    """
    eerepr.initialize(max_cache_size=None)

    _get_cached_repr.cache_clear()

    assert _get_cached_repr.cache_info().misses == 0
    x = ee.List([0, 1, 2]).shuffle(seed=False)

    _get_cached_repr(x)
    _get_cached_repr(x)

    assert _get_cached_repr.cache_info().misses == 2
