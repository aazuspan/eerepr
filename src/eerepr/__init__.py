from importlib.metadata import PackageNotFoundError, version

from eerepr.repr import initialize, options, reset

try:
    __version__ = version("eerepr")
except PackageNotFoundError:
    __version__ = "unknown"

__all__ = ["initialize", "reset", "options"]
