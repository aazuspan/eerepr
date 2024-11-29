from pathlib import Path

import ee
import pytest

from eerepr.html import convert_to_html
from tests.cache import get_info


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
        "pixel_custom": ee.Dictionary(
            dict(type="PixelType", min=10, max=255, precision="int")
        ),
        "clusterer": ee.Clusterer.wekaKMeans(2),
        "classifier": ee.Classifier.smileKNN(),
        "array": ee.Array([[1, 2], [3, 4]]),
        "confusion_matrix": ee.ConfusionMatrix(ee.Array([[1, 2], [3, 4]])),
        "kernel": ee.Kernel.gaussian(3),
        "projection": ee.Projection("EPSG:5070").atScale(100),
        "reducer": ee.Reducer.max(5),
    }


@pytest.fixture(scope="session")
def original_datadir():
    return Path(__file__).parent / "data"


@pytest.mark.parametrize("key_val", get_test_objects().items(), ids=lambda kv: kv[0])
def test_regression(key_val, data_regression):
    data_regression.check(convert_to_html(get_info(key_val[1])))
