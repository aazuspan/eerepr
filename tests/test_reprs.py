import ee
import pytest

import eerepr  # noqa: F401


def test_error():
    """Test that an object that raises on getInfo falls abck to the string repr and
    warns.
    """
    with pytest.warns(UserWarning):
        rep = ee.Projection("not a real epsg")._repr_html_()
    assert "Projection object" in rep
