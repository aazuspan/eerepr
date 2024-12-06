from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Config:
    max_cache_size: int | None = None
    max_repr_mbs: int = 100

    def update(self, **kwargs) -> Config:
        self.__dict__.update(**kwargs)
        return self
