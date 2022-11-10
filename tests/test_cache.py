from functools import _lru_cache_wrapper

import ee

import eerepr


def test_disabled_cache():
    eerepr.initialize(max_cache_size=0)
    x = ee.Number(0)
    assert not isinstance(x._repr_html_, _lru_cache_wrapper)


def test_nondeterministic_caching():
    """ee.List.shuffle(seed=False) is nondeterministic. Make sure it misses the cache."""
    eerepr.initialize(max_cache_size=None)
    cache = eerepr.repr._repr_html_

    cache.cache_clear()

    assert cache.cache_info().misses == 0
    x = ee.List([0, 1, 2]).shuffle(seed=False)
    x._repr_html_()
    x._repr_html_()
    assert cache.cache_info().misses == 2
