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


def test_nondeterministic_caching():
    """
    ee.List.shuffle(seed=False) is nondeterministic. Make sure it misses the cache.
    """
    eerepr.initialize()
    cache = eerepr.repr._repr_html_

    assert cache.cache_info().misses == 0
    x = ee.List([0, 1, 2]).shuffle(seed=False)
    x._repr_html_()
    x._repr_html_()
    assert cache.cache_info().misses == 2
