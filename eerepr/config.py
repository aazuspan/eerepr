import json


class Config:
    def __init__(self, max_cache_size, max_repr_mbs):
        self.max_cache_size = max_cache_size
        self.max_repr_mbs = max_repr_mbs

    def __repr__(self):
        return json.dumps(self.__dict__, indent=2)


options = Config(
    max_cache_size=None,
    max_repr_mbs=100,
)
