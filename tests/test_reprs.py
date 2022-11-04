import ee
import pytest

import eerepr


def test_image():
    rep = ee.Image.constant(0).set("system:id", "foo")._repr_html_()
    assert "Image foo (1 band)" in rep
    assert "bands: List (1 element)" in rep
    assert "crs_transform: [1, 0, 0, 0, 1, 0]" in rep


def test_imagecollection():
    rep = (
        ee.ImageCollection(
            [
                ee.Image.constant(0),
                ee.Image.constant(1),
            ]
        )
        .set("test_prop", 42)
        ._repr_html_()
    )

    assert "ImageCollection (2 elements)" in rep
    assert "properties: Object (1 property)" in rep
    assert "features: List (2 elements)" in rep


def test_feature():
    rep = ee.Feature(
        geom=ee.Geometry.Point([0, 0]), opt_properties={"foo": "bar"}
    )._repr_html_()

    assert "Feature (Point, 1 property)" in rep


def test_featurecollection():
    feat = ee.Feature(geom=ee.Geometry.Point([0, 0]), opt_properties={"foo": "bar"})
    rep = ee.FeatureCollection([feat])._repr_html_()
    assert "FeatureCollection (1 element, 2 columns)" in rep


def test_date():
    rep = ee.Date("2021-03-27T14:01:07")._repr_html_()

    assert "Date" in rep
    assert "2021-03-27 14:01:07" in rep


def test_filter():
    rep = ee.Filter.eq("foo", "bar")._repr_html_()

    assert "Filter.eq" in rep


def test_dict():
    rep = ee.Dictionary({"foo": "bar"})._repr_html_()

    assert "Object (1 property)" in rep


def test_list():
    short_rep = ee.List([1, 2, 3, 4])._repr_html_()
    assert "[1, 2, 3, 4]" in short_rep

    long_rep = ee.List.sequence(0, 20, 1)._repr_html_()
    assert "List (21 elements)" in long_rep


def test_string():
    rep = ee.String("13th Warrior is an underrated movie")._repr_html_()
    assert "13th Warrior is an underrated movie" in rep


def test_number():
    rep = ee.Number(42)._repr_html_()
    assert "42" in rep


def test_point():
    rep = ee.Geometry.Point([1.112312, 2])._repr_html_()
    assert "Point (1.11, 2.00)" in rep


def test_multipoint():
    rep = ee.Geometry.MultiPoint([[1, 1], [2, 2]])._repr_html_()
    assert "MultiPoint (2 vertices)" in rep


def test_linestring():
    rep = ee.Geometry.LineString([[1, 1], [2, 2], [3, 3]])._repr_html_()
    assert "LineString (3 vertices)" in rep


def test_multilinestring():
    rep = ee.Geometry.MultiLineString([[[0, 0], [1, 1]]])._repr_html_()
    assert "MultiLineString" in rep


def test_polygon():
    rep = ee.Geometry.Polygon([[0, 0], [1, 1], [2, 2], [0, 0]])._repr_html_()
    assert "Polygon (4 vertices)" in rep


def test_multipolygon():
    rep = ee.Geometry.MultiPolygon(
        [
            [[0, 0], [1, 1], [2, 2], [0, 0]],
            [[4, 6], [3, 2], [1, 2], [4, 6]],
        ]
    )._repr_html_()
    assert "MultiPolygon (8 vertices)" in rep


def test_linearring():
    rep = ee.Geometry.LinearRing([[0, 0], [1, 1], [2, 2], [0, 0]])._repr_html_()
    assert "LinearRing (4 vertices)" in rep


def test_pixel_types():
    assert "float" in ee.PixelType.float()._repr_html_()
    assert "double" in ee.PixelType.double()._repr_html_()
    assert "signed int8" in ee.PixelType.int8()._repr_html_()
    assert "unsigned int8" in ee.PixelType.uint8()._repr_html_()
    assert "signed int16" in ee.PixelType.int16()._repr_html_()
    assert "unsigned int16" in ee.PixelType.uint16()._repr_html_()
    assert "signed int32" in ee.PixelType.int32()._repr_html_()
    assert "unsigned int32" in ee.PixelType.uint32()._repr_html_()
    assert "signed int64" in ee.PixelType.int64()._repr_html_()

    custom_type = dict(type="PixelType", min=10, max=255, precision="int")
    assert "int ∈ [10, 255]" in ee.Dictionary(custom_type)._repr_html_()


def test_band():
    band_id = "B1"
    data_type = {"type": "PixelType", "precision": "int", "min": 0, "max": 65535}
    dimensions = [1830, 1830]
    crs = "EPSG:32610"

    assert (
        '"B1", unsigned int16, EPSG:32610, 1830x1830 px'
        in ee.Dictionary(
            {
                "id": band_id,
                "data_type": data_type,
                "dimensions": dimensions,
                "crs": crs,
            }
        )._repr_html_()
    )

    assert (
        '"B1", unsigned int16'
        in ee.Dictionary(
            {
                "id": band_id,
                "data_type": data_type,
            }
        )._repr_html_()
    )


def test_daterange():
    rep = ee.DateRange("2020-01-01T21:01:10", "2022-03-01T14:32:11")._repr_html_()
    assert "DateRange [2020-01-01 21:01:10, 2022-03-01 14:32:11]" in rep


def test_typed_obj():
    rep = ee.Dictionary({"type": "Foo", "id": "bar"})._repr_html_()
    assert "Foo bar" in rep


def test_error():
    """Test that an object that raises on getInfo falls abck to the string repr and warns."""
    with pytest.warns(UserWarning):
        rep = ee.Projection("not a real epsg")._repr_html_()
    assert "ee.Projection object" in rep
