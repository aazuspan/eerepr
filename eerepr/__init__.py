import ee

from eerepr.config import options
from eerepr.repr import initialize

__version__ = "0.0.4"
__all__ = ["clear_cache", "initialize", "options"]

initialize(max_cache_size=options.max_cache_size)
