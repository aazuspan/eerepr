import ee

from eerepr.repr import initialize
from eerepr.config import options

__version__ = '0.0.2'
__all__ = ['clear_cache', 'initialize', 'options']

initialize(max_cache_size=options.max_cache_size)
