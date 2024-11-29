import ee
import pytest

import eerepr  # noqa: F401
from eerepr.repr import _repr_html_


def test_error():
    """Test that an object that raises on getInfo falls back to the string repr and
    warns.
    """
    eerepr.initialize()
    with pytest.warns(UserWarning):
        rep = ee.Projection("not a real epsg")._repr_html_()
    assert "Projection object" in rep
    eerepr.reset()


def test_full_repr(data_regression):
    """Regression test the full HTML repr (with CSS and JS) of a nested EE object."""
    from tests.test_html import get_test_objects

    objects = get_test_objects().items()
    rendered = _repr_html_(ee.List([obj[1] for obj in objects]))
    data_regression.check(rendered)


def test_initialize_and_reset():
    """Test that _repr_html_ is added and removed by eerepr."""
    assert not hasattr(ee.Number(1), "_repr_html_")
    eerepr.initialize()
    assert hasattr(ee.Number(1), "_repr_html_")
    eerepr.reset()
    assert not hasattr(ee.Number(1), "_repr_html_")


def test_existing_repr_html():
    """If an object already has a _repr_html_, eerepr shouldn't touch it."""

    class SpecialNumber(ee.Number):
        def _repr_html_(self):
            return "foo"

    obj = SpecialNumber(0)

    # initialize shouldn't overwrite the existing repr
    eerepr.initialize()
    assert obj._repr_html_() == "foo"

    # reset shouldn't remove the existing repr
    eerepr.reset()
    assert obj._repr_html_() == "foo"
