from functools import _lru_cache_wrapper

import ee

import eerepr


def test_clear_cache():
    x = ee.Number(0)
    x._repr_html_()
    assert x._repr_html_.cache_info().currsize == 1

    eerepr.clear_cache()
    assert x._repr_html_.cache_info().currsize == 0


def test_disabled_cache():
    eerepr.initialize(max_cache_size=0)
    x = ee.Number(0)
    assert not isinstance(x._repr_html_, _lru_cache_wrapper)

    # This shouldn't break
    eerepr.clear_cache()
