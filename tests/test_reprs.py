import ee
import pytest

import eerepr  # noqa: F401
from eerepr.repr import _repr_html_


def test_error():
    """Test that an object that raises on getInfo falls back to the string repr and
    warns.
    """
    with pytest.warns(UserWarning):
        rep = ee.Projection("not a real epsg")._repr_html_()
    assert "Projection object" in rep


def test_full_repr(data_regression):
    """Regression test the full HTML repr (with CSS and JS) of a nested EE object."""
    from tests.test_html import get_test_objects

    objects = get_test_objects().items()
    rendered = _repr_html_(ee.List([obj[1] for obj in objects]))
    data_regression.check(rendered)
