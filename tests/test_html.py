import ee

from eerepr.html import convert_to_html
from tests.cache import get_info


def test_image():
    obj = ee.Image.constant(0).set("system:id", "foo")
    info = get_info(obj)
    rep = convert_to_html(info)
    assert "Image foo (1 band)" in rep
    assert "bands: List (1 element)" in rep
    assert "crs_transform: [1, 0, 0, 0, 1, 0]" in rep


def test_imagecollection():
    obj = ee.ImageCollection(
        [
            ee.Image.constant(0),
            ee.Image.constant(1),
        ]
    ).set("test_prop", 42)
    info = get_info(obj)
    rep = convert_to_html(info)

    assert "ImageCollection (2 elements)" in rep
    assert "properties: Object (1 property)" in rep
    assert "features: List (2 elements)" in rep


def test_feature():
    obj = ee.Feature(geom=ee.Geometry.Point([0, 0]), opt_properties={"foo": "bar"})
    info = get_info(obj)
    rep = convert_to_html(info)

    assert "Feature (Point, 1 property)" in rep


def test_empty_feature():
    obj = ee.Feature(None)
    info = get_info(obj)
    rep = convert_to_html(info)

    assert "Feature (0 properties)" in rep


def test_featurecollection():
    feat = ee.Feature(geom=ee.Geometry.Point([0, 0]), opt_properties={"foo": "bar"})
    obj = ee.FeatureCollection([feat])
    info = get_info(obj)
    rep = convert_to_html(info)

    assert "FeatureCollection (1 element, 2 columns)" in rep


def test_date():
    obj = ee.Date("2021-03-27T14:01:07")
    info = get_info(obj)
    rep = convert_to_html(info)

    assert "Date" in rep
    assert "2021-03-27 14:01:07" in rep


def test_filter():
    obj = ee.Filter.eq("foo", "bar")
    info = get_info(obj)
    rep = convert_to_html(info)

    assert "Filter.eq" in rep


def test_dict():
    obj = ee.Dictionary({"foo": "bar"})
    info = get_info(obj)
    rep = convert_to_html(info)

    assert "Object (1 property)" in rep


def test_list():
    short_obj = ee.List([1, 2, 3, 4])
    short_info = get_info(short_obj)
    short_rep = convert_to_html(short_info)
    assert "[1, 2, 3, 4]" in short_rep

    long_obj = ee.List.sequence(0, 20, 1)
    long_info = get_info(long_obj)
    long_rep = convert_to_html(long_info)
    assert "List (21 elements)" in long_rep


def test_string():
    obj = ee.String("13th Warrior is an underrated movie")
    info = get_info(obj)
    rep = convert_to_html(info)

    assert "13th Warrior is an underrated movie" in rep


def test_number():
    obj = ee.Number(42)
    info = get_info(obj)
    rep = convert_to_html(info)

    assert "42" in rep


def test_point():
    obj = ee.Geometry.Point([1.112312, 2])
    info = get_info(obj)
    rep = convert_to_html(info)

    assert "Point (1.11, 2.00)" in rep


def test_multipoint():
    obj = ee.Geometry.MultiPoint([[1, 1], [2, 2]])
    info = get_info(obj)
    rep = convert_to_html(info)

    assert "MultiPoint (2 vertices)" in rep


def test_linestring():
    obj = ee.Geometry.LineString([[1, 1], [2, 2], [3, 3]])
    info = get_info(obj)
    rep = convert_to_html(info)

    assert "LineString (3 vertices)" in rep


def test_multilinestring():
    obj = ee.Geometry.MultiLineString([[[0, 0], [1, 1]]])
    info = get_info(obj)
    rep = convert_to_html(info)

    assert "MultiLineString" in rep


def test_polygon():
    obj = ee.Geometry.Polygon([[0, 0], [1, 1], [2, 2], [0, 0]])
    info = get_info(obj)
    rep = convert_to_html(info)

    assert "Polygon (4 vertices)" in rep


def test_multipolygon():
    obj = ee.Geometry.MultiPolygon(
        [
            [[0, 0], [1, 1], [2, 2], [0, 0]],
            [[4, 6], [3, 2], [1, 2], [4, 6]],
        ]
    )
    info = get_info(obj)
    rep = convert_to_html(info)

    assert "MultiPolygon (8 vertices)" in rep


def test_linearring():
    obj = ee.Geometry.LinearRing([[0, 0], [1, 1], [2, 2], [0, 0]])
    info = get_info(obj)
    rep = convert_to_html(info)

    assert "LinearRing (4 vertices)" in rep


def test_daterange():
    obj = ee.DateRange("2020-01-01T21:01:10", "2022-03-01T14:32:11")
    info = get_info(obj)
    rep = convert_to_html(info)

    assert "DateRange [2020-01-01 21:01:10, 2022-03-01 14:32:11]" in rep


def test_typed_obj():
    obj = ee.Dictionary({"type": "Foo", "id": "bar"})
    info = get_info(obj)
    rep = convert_to_html(info)

    assert "Foo bar" in rep


def test_band():
    band_id = "B1"
    data_type = {"type": "PixelType", "precision": "int", "min": 0, "max": 65535}
    dimensions = [1830, 1830]
    crs = "EPSG:32610"

    band1 = ee.Dictionary(
        {
            "id": band_id,
            "data_type": data_type,
            "dimensions": dimensions,
            "crs": crs,
        }
    )
    band1_info = get_info(band1)
    band1_rep = convert_to_html(band1_info)
    assert '"B1", unsigned int16, EPSG:32610, 1830x1830 px' in band1_rep

    band2 = ee.Dictionary(
        {
            "id": band_id,
            "data_type": data_type,
        }
    )
    band2_info = get_info(band2)
    band2_rep = convert_to_html(band2_info)
    assert '"B1", unsigned int16' in band2_rep


def test_pixel_types():
    assert "float" in convert_to_html(get_info(ee.PixelType.float()))
    assert "double" in convert_to_html(get_info(ee.PixelType.double()))
    assert "signed int8" in convert_to_html(get_info(ee.PixelType.int8()))
    assert "unsigned int8" in convert_to_html(get_info(ee.PixelType.uint8()))
    assert "signed int16" in convert_to_html(get_info(ee.PixelType.int16()))
    assert "unsigned int16" in convert_to_html(get_info(ee.PixelType.uint16()))
    assert "signed int32" in convert_to_html(get_info(ee.PixelType.int32()))
    assert "unsigned int32" in convert_to_html(get_info(ee.PixelType.uint32()))
    assert "signed int64" in convert_to_html(get_info(ee.PixelType.int64()))

    custom_type = dict(type="PixelType", min=10, max=255, precision="int")
    assert "int ∈ [10, 255]" in convert_to_html(get_info(ee.Dictionary(custom_type)))
