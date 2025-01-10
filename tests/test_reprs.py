import ee

import eerepr


def test_full_repr(data_regression):
    """Regression test the full HTML repr (with CSS and JS) of a nested EE object."""
    from tests.test_html import get_test_objects

    eerepr.initialize()

    objects = get_test_objects().values()
    rendered = ee.List([obj for obj in objects])._repr_html_()
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


def test_scripts_sanitized():
    """Test that scripts within objects are escaped."""
    eerepr.initialize()

    script_injection = "<script>alert('foo')</script>"

    obj = ee.String(script_injection)
    assert "<script>" not in obj._repr_html_()

    obj = ee.List([script_injection])
    assert "<script>" not in obj._repr_html_()

    obj = ee.Dictionary({script_injection: script_injection, "type": script_injection})
    assert "<script>" not in obj._repr_html_()
