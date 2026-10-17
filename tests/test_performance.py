import json
from pathlib import Path

import pytest

from eerepr.repr import _cached_repr


class MockObject:
    """Mock an Earth Engine object to return getInfo from memory."""

    def __init__(self, data):
        self._data = data

    def getInfo(self):
        return self._data

    def serialize(self):
        """Dummy serialization that passes a deterministic heuristic."""
        return ""


@pytest.fixture(scope="module")
def image_collection():
    data_path = Path(__file__).parent / "data/sentinel2_sample.json"
    with open(data_path) as f:
        data = json.load(f)
    return MockObject(data)


@pytest.fixture(scope="module")
def feature_collection():
    data_path = Path(__file__).parent / "data/powerplant_sample.json"
    with open(data_path) as f:
        data = json.load(f)
    return MockObject(data)


@pytest.mark.benchmark
def test_image_collection_repr_benchmark(image_collection, benchmark):
    html = benchmark(_cached_repr.__wrapped__, image_collection)
    assert len(html) > 1e6


@pytest.mark.benchmark
def test_feature_collection_repr_benchmark(feature_collection, benchmark):
    html = benchmark(_cached_repr.__wrapped__, feature_collection)
    assert len(html) > 1e6
