from functools import _lru_cache_wrapper

import ee
import pytest

import eerepr


@pytest.mark.parametrize("max_cache_size", [0, None, 1, 10])
def test_cache_params(max_cache_size):
    """
    Test that the cache size is correctly set, or disabled when max_cache_size=0.
    """
    eerepr.initialize(max_cache_size=max_cache_size)

    if max_cache_size == 0:
        assert not isinstance(eerepr.repr._repr_html_, _lru_cache_wrapper)
    else:
        assert eerepr.repr._repr_html_.cache_info().maxsize == max_cache_size


def test_max_repr_mbs():
    """
    Test that exceeding max_repr_mbs triggers a warning and falls back to string repr.
    """
    eerepr.initialize(max_repr_mbs=0)

    with pytest.warns(UserWarning, match="HTML repr size"):
        rep = ee.Image.constant(0).set("system:id", "foo")._repr_html_()
        assert "<pre>" in rep


def test_on_error():
    """Test that errors are correctly warned or raised based on on_error."""
    invalid_obj = ee.Projection("not a real epsg")

    eerepr.initialize(on_error="warn")
    with pytest.warns(UserWarning, match="Getting info failed"):
        rep = invalid_obj._repr_html_()
        assert "Projection object" in rep

    eerepr.initialize(on_error="raise")
    with pytest.raises(ee.EEException):
        invalid_obj._repr_html_()
