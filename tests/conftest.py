import json
import os
import warnings
from collections import UserDict
from pathlib import Path

import ee
import pytest

import eerepr


class ObjectCache(UserDict):
    """
    A cache that reads and writes to a local JSON file.
    """

    CACHE_DIR = Path(__file__).parent / "data/"
    CACHE_PATH = CACHE_DIR / ".cache.json"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.modified = False

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.modified = True

    def __delitem__(self, key):
        super().__delitem__(key)
        self.modified = True

    @classmethod
    def load_from_disk(cls):
        if not cls.CACHE_PATH.exists():
            return ObjectCache()

        with open(cls.CACHE_PATH) as src:
            try:
                return ObjectCache(json.load(src))
            except json.JSONDecodeError:
                warnings.warn("Failed to load cache file.", stacklevel=2)
                return ObjectCache()

    def write_to_disk(self):
        if not self.CACHE_PATH.exists():
            self.CACHE_DIR.mkdir(parents=True, exist_ok=True)
            warnings.warn(
                f"Creating new cache file at {self.CACHE_PATH}.", stacklevel=2
            )

        with open(self.CACHE_PATH, "w") as dst:
            warnings.warn("Saving modified cache to disk.", stacklevel=2)
            json.dump(self.data, dst)


@pytest.fixture(scope="session")
def object_cache():
    """Fixture to access the in-memory object cache for the session."""
    session_cache = ObjectCache.load_from_disk()

    yield session_cache

    if session_cache.modified:
        session_cache.write_to_disk()


def pytest_sessionstart(session):
    if os.environ.get("GITHUB_ACTIONS"):
        service_account = os.environ.get("EE_SERVICE_ACCOUNT")
        credentials = ee.ServiceAccountCredentials(None, key_data=service_account)
    else:
        credentials = "persistent"

    ee.Initialize(credentials=credentials)


@pytest.fixture(autouse=True)
def reset_eerepr():
    """Reset eerepr after each test to avoid inconsistent state."""
    yield
    eerepr.reset()


@pytest.fixture(scope="session")
def original_datadir():
    """Set the pytest-regressions directory."""
    return Path(__file__).parent / "data"


@pytest.fixture(autouse=True)
def mock_getinfo(mocker, object_cache):
    """
    Mock `getInfo` to load Earth Engine object info from a local cache, if available.

    Info is retrieved from a local JSON file using the serialized object as the key. If
    the data does not exist locally, it is loaded from Earth Engine servers and stored
    for future use. If the server returns an error, the error is stored in the cache and
    raised on subsequent calls.
    """
    # Store the original getInfo so that the mocked function doesn't call itself
    get_server_info = ee.ComputedObject.getInfo

    def get_cached_info(obj: ee.ComputedObject) -> dict:
        serialized = obj.serialize()

        if serialized not in object_cache:
            warnings.warn("Fetching and caching new object from server.", stacklevel=2)
            try:
                info = get_server_info(obj)
            except Exception as e:
                # Errors should be stored to allow raising from the cache without
                # needing to re-fetch the object
                info = {"error": str(e)}

            object_cache[serialized] = info

        # Raise on error (including cached) to simulate getInfo behavior
        if (
            isinstance(object_cache[serialized], dict)
            and "error" in object_cache[serialized]
        ):
            raise ee.EEException(object_cache[serialized]["error"])

        return object_cache[serialized]

    mocker.patch(
        "ee.ComputedObject.getInfo", side_effect=get_cached_info, autospec=True
    )
