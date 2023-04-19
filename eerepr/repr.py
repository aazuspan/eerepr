import uuid
from functools import _lru_cache_wrapper, lru_cache
from typing import Callable, Type, Union
import threading
import anywidget
import traitlets
import time
from warnings import warn

import ee

from eerepr.config import options
from eerepr.html import build_object_html, build_loading_html, build_error_html, build_fallback_html
from eerepr.utils import is_nondeterministic, load_css, load_js


# Track which reprs have been set so we can overwrite them if needed.
reprs_set = set()
EEObject = Union[ee.Element, ee.ComputedObject]


def _attach_repr(cls: Type, repr: Callable) -> None:
    """Add a custom repr method to an EE class. Only overwrite the method if it was set by this function."""
    if not hasattr(cls, "_ipython_display_") or cls.__name__ in reprs_set:
        reprs_set.update([cls.__name__])
        setattr(cls, "_ipython_display_", repr)


def _ipython_display_(obj: EEObject, **kwargs) -> str:
    """IPython display wrapper for Earth Engine objects."""
    return EEReprWidget(obj)._ipython_display_(**kwargs)


@lru_cache(maxsize=None)
def _get_cached_repr(obj: EEObject) -> str:
    """Build or retrieve an HTML repr from an Earth Engine object."""
    if is_nondeterministic(obj):
        # Prevent caching of non-deterministic objects (e.g. ee.List([]).shuffle(False)))
        setattr(obj, "_eerepr_id", uuid.uuid4())

    try:
        info = obj.getInfo()
        content = f"<ul>{build_object_html(info)}</ul>"
    except ee.EEException as e:
        content = build_error_html(e)

    return content


def initialize(max_cache_size=None) -> None:
    """Attach repr methods to EE objects and set the cache size.

    Re-running this function will reset the cache.

    Parameters
    ----------
    max_cache_size : int, optional
        The maximum number of EE objects to cache. If None, the cache size is unlimited. Set to 0
        to disable caching.
    """
    global _get_cached_repr
    # Unwrap from the LRU cache so we can reset it
    if isinstance(_get_cached_repr, _lru_cache_wrapper):
        _get_cached_repr = _get_cached_repr.__wrapped__

    # If caching is enabled, rewrap in a new LRU cache
    if max_cache_size != 0:
        _get_cached_repr = lru_cache(maxsize=max_cache_size)(_get_cached_repr)

    for cls in [ee.Element, ee.ComputedObject]:
        _attach_repr(cls, _ipython_display_)


class EEReprWidget(anywidget.AnyWidget):
    _esm = load_js()
    _css = load_css()
    
    content = traitlets.Unicode().tag(sync=True)

    def __init__(self, obj: EEObject, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.obj = obj
        self.set_content(build_loading_html(obj))
        threading.Thread(target=self.update_content).start()

    def update_content(self) -> None:
        """
        Update the widget content with the cached repr. Currently, this
        implementation delays as needed to give time for communication between
        the kernel and the frontend to complete.
        """
        start = time.time()
        rep = _get_cached_repr(self.obj)
        elapsed = time.time() - start
        if elapsed < options.communication_delay:
            time.sleep(options.communication_delay - elapsed)

        self.set_content(rep)

    def set_content(self, content: str) -> None:
        """Set the widget content, checking content size to avoid crashes from huge reprs."""
        mbs = len(content) / 1e6
        if mbs > options.max_repr_mbs:
            warn(
                message=(
                    f"HTML repr size ({mbs:.0f}mB) exceeds maximum ({options.max_repr_mbs:.0f}mB), falling"
                    " back to string repr. You can set `eerepr.options.max_repr_mbs` to display larger"
                    " objects, but this may cause performance issues."
                )
            )
            content = build_fallback_html(self.obj)

        self.content = content

    def _ipython_display_(self, **kwargs):
        """
        Display the widget in an IPython kernel.

        We dynamically choose _ipython_display_ or _repr_mimebundle_ based on which
        is supported by the widget, which is determined by anywidget based on the
        environment. See https://github.com/manzt/anywidget/issues/48 for details.
        """

        if hasattr(super(), "_ipython_display_"):
            # ipywidgets v7
            super()._ipython_display_(**kwargs)
        else:
            from IPython.display import display
            import ipywidgets
            # ipywidgets v8
            data = ipywidgets.DOMWidget._repr_mimebundle_(self, **kwargs)
            display(data, raw=True)
