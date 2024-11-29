import json
from pathlib import Path

import ee

CACHE_DIR = Path(__file__).parent / "data/"
CACHE_PATH = CACHE_DIR / ".cache.json"


def get_info(obj: ee.ComputedObject) -> dict:
    """Load client-side info for an Earth Engine object.

    Info is retrieved (if available) from a local JSON file using the serialized
    object as the key. If the data does not exist locally, it is loaded from Earth
    Engine servers and stored for future use.
    """
    serialized = obj.serialize()

    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    try:
        with open(CACHE_PATH) as src:
            existing_data = json.load(src)

    # File is missing or unreadable
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = {}
        with open(CACHE_PATH, "w") as dst:
            json.dump(existing_data, dst)

    # File exists, but info does not
    if serialized not in existing_data:
        with open(CACHE_PATH, "w") as dst:
            existing_data[serialized] = obj.getInfo()
            json.dump(existing_data, dst, indent=2)

    return existing_data[serialized]
