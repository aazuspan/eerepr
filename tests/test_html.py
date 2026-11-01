import ee
import pytest

from eerepr.html import _summarize_pixeltype, convert_to_html

from . import factory


def get_test_objects() -> list:
    return {
        "constant_image": ee.Image.constant(0).set("system:id", "foo"),
        "image_collection": ee.ImageCollection(
            [
                ee.Image.constant(0),
                ee.Image.constant(1),
            ]
        ).set("test_prop", 42),
        "feature": ee.Feature(
            geom=ee.Geometry.Point([0, 0]), opt_properties={"foo": "bar"}
        ),
        "null_feature": ee.Feature(None),
        "feature_collection": ee.FeatureCollection(
            [ee.Feature(geom=ee.Geometry.Point([0, 0]), opt_properties={"foo": "bar"})]
        ),
        "date": ee.Date("2021-03-27T14:01:07"),
        "filter": ee.Filter.eq("foo", "bar"),
        "dict": ee.Dictionary({"foo": "bar"}),
        "short_list": ee.List([1, 2, 3, 4]),
        "long_list": ee.List.sequence(0, 20, 1),
        "string": ee.String("13th Warrior is an underrated movie"),
        "number": ee.Number(42),
        "point": ee.Geometry.Point([1.112312, 2]),
        "multipoint": ee.Geometry.MultiPoint([[1, 1], [2, 2]]),
        "linestring": ee.Geometry.LineString([[1, 1], [2, 2], [3, 3]]),
        "multilinestring": ee.Geometry.MultiLineString([[[0, 0], [1, 1]]]),
        "polygon": ee.Geometry.Polygon([[0, 0], [1, 1], [2, 2], [0, 0]]),
        "multipolygon": ee.Geometry.MultiPolygon(
            [
                [[0, 0], [1, 1], [2, 2], [0, 0]],
                [[4, 6], [3, 2], [1, 2], [4, 6]],
            ]
        ),
        "linearring": ee.Geometry.LinearRing([[0, 0], [1, 1], [2, 2], [0, 0]]),
        "daterange": ee.DateRange("2020-01-01T21:01:10", "2022-03-01T14:32:11"),
        "type_dict": ee.Dictionary({"type": "Foo", "id": "bar"}),
        "band_dict": ee.Dictionary(
            {
                "id": "B1",
                "data_type": {
                    "type": "PixelType",
                    "precision": "int",
                    "min": 0,
                    "max": 65535,
                },
                "dimensions": [1830, 1830],
                "crs": "EPSG:32610",
            }
        ),
        "unbounded_band_dict": ee.Dictionary(
            {
                "id": "B1",
                "data_type": {
                    "type": "PixelType",
                    "precision": "int",
                    "min": 0,
                    "max": 65535,
                },
            }
        ),
        "pixel_float": ee.PixelType.float(),
        "pixel_double": ee.PixelType.double(),
        "pixel_int8": ee.PixelType.int8(),
        "pixel_uint8": ee.PixelType.uint8(),
        "pixel_int16": ee.PixelType.int16(),
        "pixel_uint16": ee.PixelType.uint16(),
        "pixel_int32": ee.PixelType.int32(),
        "pixel_uint32": ee.PixelType.uint32(),
        "pixel_int64": ee.PixelType.int64(),
        "pixel_custom": ee.PixelType(precision="int", minValue=10, maxValue=255),
        "pixel_1_dimension": ee.PixelType(
            precision="int", minValue=0, maxValue=255, dimensions=1
        ),
        "pixel_3_dimensions": ee.PixelType(
            precision="int", minValue=0, maxValue=10, dimensions=3
        ),
        "clusterer": ee.Clusterer.wekaKMeans(2),
        "classifier": ee.Classifier.smileKNN(),
        "array": ee.Array([[1, 2], [3, 4]]),
        "confusion_matrix": ee.ConfusionMatrix(ee.Array([[1, 2], [3, 4]])),
        "kernel": ee.Kernel.gaussian(3),
        "projection": ee.Projection("EPSG:5070").atScale(100),
        # A WKT string includes whitespace that should be preserved in a leaf element
        "wkt_string": ee.Projection("EPSG:4326").wkt(),
        "reducer": ee.Reducer.max(5),
    }


@pytest.mark.parametrize("key_val", get_test_objects().items(), ids=lambda kv: kv[0])
def test_regression_objects(key_val, data_regression):
    """Test the HTML repr of various EE objects."""
    data_regression.check(convert_to_html(key_val[1].getInfo()))


@pytest.mark.parametrize("precision", ["double", "float"])
def test_summarize_float_pixel_types_return_range(precision: str):
    """'float' and 'double' used to just return precision in the Code Editor, but now
    return their range also.
    """
    pixel_type = factory.PixelType(precision=precision, max=255, min=0)
    assert _summarize_pixeltype(pixel_type) == f"{precision} ∈ [0, 255]"


@pytest.mark.parametrize("precision", ["int", "double", "float"])
@pytest.mark.parametrize("drop", ["min", "max"])
def test_summarize_pixel_type_missing_min_or_max_returns_precision(
    drop: str, precision: str
):
    pixel_type = factory.PixelType(precision=precision, min=0, max=255)
    del pixel_type[drop]
    assert _summarize_pixeltype(pixel_type) == precision


@pytest.mark.parametrize("precision", ["int", "double", "float"])
@pytest.mark.parametrize("dimensions", [0, None])
def test_summarize_pixel_type_with_0_dimensions(precision: str, dimensions: int | None):
    """dimensions=0 or None drop the dimension suffix"""
    pixel_type = factory.PixelType(precision=precision, dimensions=dimensions)
    assert _summarize_pixeltype(pixel_type) == precision


@pytest.mark.parametrize("precision", ["int", "double", "float"])
def test_summarize_pixel_type_with_1_dimension(precision: str):
    pixel_type = factory.PixelType(precision=precision, dimensions=1)
    assert _summarize_pixeltype(pixel_type) == f"{precision}, 1 dimension"


@pytest.mark.parametrize("precision", ["int", "double", "float"])
def test_summarize_pixel_type_with_n_dimensions(precision: str):
    pixel_type = factory.PixelType(precision=precision, dimensions=3)
    assert _summarize_pixeltype(pixel_type) == f"{precision}, 3 dimensions"


@pytest.mark.parametrize("precision", ["int", "double", "float"])
@pytest.mark.parametrize("dimensions", ["foo", [1, 2, 3], {"a": 0, "b": 1, "c": 2}])
def test_summarize_pixel_type_with_sized_dimensions(
    precision: str, dimensions: str | list
):
    """A pixel type with non-numeric dimensions use the length, if available."""
    pixel_type = factory.PixelType(precision=precision, dimensions=dimensions)
    assert _summarize_pixeltype(pixel_type) == f"{precision}, 3 dimensions"
