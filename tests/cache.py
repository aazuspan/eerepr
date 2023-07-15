import json
import os

CACHE_DIR = "./tests/data/"
CACHE_PATH = CACHE_DIR + "data.json"


def get_info(obj):
    """Load client-side info for an Earth Engine object.

    Info is retrieved (if available) from a local JSON file using the serialized
    object as the key. If the data does not exist locally, it is loaded from Earth
    Engine servers and stored for future use.
    """
    serialized = obj.serialize()

    if not os.path.isdir("./tests/data"):
        os.mkdir("./tests/data")

    try:
        with open("./tests/data/data.json") as src:
            existing_data = json.load(src)

    # File is missing or unreadable
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = {}
        with open("./tests/data/data.json", "w") as dst:
            json.dump(existing_data, dst)

    # File exists, but info does not
    if serialized not in existing_data:
        with open("./tests/data/data.json", "w") as dst:
            existing_data[serialized] = obj.getInfo()
            json.dump(existing_data, dst, indent=2)

    return existing_data[serialized]
