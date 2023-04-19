import json


class Config:
    def __init__(self, max_cache_size, max_repr_mbs, communication_delay):
        self.max_cache_size = max_cache_size
        self.max_repr_mbs = max_repr_mbs
        self.communication_delay = communication_delay

    def __repr__(self):
        return json.dumps(self.__dict__, indent=2)


options = Config(
    # Max number of EE objects to cache. Set to 0 to disable caching.
    max_cache_size=None,
    # Max size of repr content in MB to prevent performance issues
    max_repr_mbs=100,
    # Minimum delay in seconds before updating widgets to prevent communication timing issues.
    communication_delay=0.1,
)
