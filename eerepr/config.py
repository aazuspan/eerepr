from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


@dataclass
class Config:
    max_cache_size: int | None = None
    max_repr_mbs: int = 100
    on_error: Literal["warn", "raise"] = "warn"

    def update(self, **kwargs) -> Config:
        if "on_error" in kwargs and kwargs["on_error"] not in ["warn", "raise"]:
            raise ValueError("on_error must be 'warn' or 'raise'")

        self.__dict__.update(**kwargs)
        return self
