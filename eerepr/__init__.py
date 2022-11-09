import ee

from eerepr.repr import initialize

__version__ = '0.0.1'
__all__ = ['clear_cache', 'initialize']

MAX_CACHE_SIZE = None

initialize(max_cache_size=MAX_CACHE_SIZE)
