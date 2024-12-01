import json
import warnings
from pathlib import Path

import ee
import pytest

CACHE_DIR = Path(__file__).parent / "data/"
CACHE_PATH = CACHE_DIR / ".cache.json"


def pytest_sessionstart(session):
    ee.Initialize()


@pytest.fixture(scope="session")
def original_datadir():
    """Set the pytest-regressions directory."""
    return Path(__file__).parent / "data"


@pytest.fixture(autouse=True)
def mock_getinfo(mocker):
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

        CACHE_DIR.mkdir(parents=True, exist_ok=True)

        try:
            with open(CACHE_PATH) as src:
                existing_data = json.load(src)

        # File is missing or unreadable
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = {}
            with open(CACHE_PATH, "w") as dst:
                warnings.warn(f"Creating new cache file at {CACHE_PATH}.", stacklevel=2)
                json.dump(existing_data, dst)

        # File exists, but info does not
        if serialized not in existing_data:
            with open(CACHE_PATH, "w") as dst:
                warnings.warn(
                    "Fetching and caching new object from server.", stacklevel=2
                )
                try:
                    info = get_server_info(obj)
                except Exception as e:
                    # Errors should be stored to allow raising from the cache without
                    # needing to re-fetch the object
                    info = {"error": str(e)}

                existing_data[serialized] = info
                json.dump(existing_data, dst, indent=2)

        # Raise on error (including cached) to simulate getInfo behavior
        if (
            isinstance(existing_data[serialized], dict)
            and "error" in existing_data[serialized]
        ):
            raise ee.EEException(existing_data[serialized]["error"])

        return existing_data[serialized]

    mocker.patch(
        "ee.ComputedObject.getInfo", side_effect=get_cached_info, autospec=True
    )
