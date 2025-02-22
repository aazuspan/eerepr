import ee
import pytest

import eerepr
import eerepr.repr
from tests.test_html import get_test_objects


@pytest.mark.parametrize("obj", get_test_objects().items(), ids=lambda kv: kv[0])
def test_caching(obj):
    """
    Test that various EE objects are correctly retrieved from the cache
    """
    eerepr.initialize()
    cache = eerepr.repr._repr_html_

    obj[1]._repr_html_()
    assert cache.cache_info().hits == 0
    obj[1]._repr_html_()
    assert cache.cache_info().hits == 1


def test_nondeterministic_uncached():
    """
    ee.List.shuffle(seed=False) is nondeterministic. Make sure it isn't cached.
    """
    eerepr.initialize()
    cache = eerepr.repr._repr_html_

    x = ee.List([0, 1, 2]).shuffle(seed=False)
    x._repr_html_()
    assert cache.cache_info().currsize == 0


def test_reset_cache():
    """Test that the cache is correctly reset."""
    eerepr.initialize()
    cache = eerepr.repr._repr_html_
    ee.Number(42)._repr_html_()
    assert cache.cache_info().currsize == 1
    eerepr.reset()
    assert cache.cache_info().currsize == 0
