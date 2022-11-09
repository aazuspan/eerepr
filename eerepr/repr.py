from functools import _lru_cache_wrapper, lru_cache
from html import escape
from importlib.resources import read_text
from typing import Callable, Type, Union
from warnings import warn

import ee

from eerepr.html import convert_to_html

REPR_HTML = "_repr_html_"
# Track which html reprs have been set so we can overwrite them if needed.
reprs_set = set()


@lru_cache(maxsize=None)
def _load_css():
    return read_text("eerepr.static.css", "style.css")


@lru_cache(maxsize=None)
def _load_js():
    """
    Note: JS is only needed because the CSS `:has()` selector isn't well supported yet, preventing
    a pure CSS solution to the collapsible lists.
    """
    return read_text("eerepr.static.js", "script.js")


def _attach_html_repr(cls: Type, repr: Callable) -> None:
    """Add a HTML repr method to an EE class. Only overwrite the method if it was set by this function."""
    if not hasattr(cls, REPR_HTML) or cls.__name__ in reprs_set:
        reprs_set.update([cls.__name__])
        setattr(cls, REPR_HTML, repr)


def _ee_repr(obj: Union[ee.Element, ee.ComputedObject]) -> str:
    """Generate an HTML representation of an EE object."""
    try:
        info = obj.getInfo()
    # Fall back to a string repr if getInfo fails
    except ee.EEException as e:
        warn(f"Getting info failed with: '{e}'. Falling back to string repr.")
        return f"<pre>{escape(repr(obj))}</pre>"

    css = _load_css()
    js = _load_js()
    body = convert_to_html(info)

    return (
        "<div>"
        f"<style>{css}</style>"
        f"<div class='eerepr'>"
        f"<ul>{body}</ul>"
        "</div>"
        f"<script>{js}</script>"
        "</div>"
    )


def initialize(max_cache_size=None) -> _lru_cache_wrapper:
    """Attach HTML repr methods to EE objects.

    Re-running this function will reset the cache.

    Parameters
    ----------
    max_cache_size : int, optional
        The maximum number of EE objects to cache. If None, the cache size is unlimited. Set to 0
        to disable caching.

    Returns
    -------
    _lru_cache_wrapper
        The cache wrapper which can be used to inspect and clear the cache.
    """
    rep = (
        lru_cache(maxsize=max_cache_size)(_ee_repr) if max_cache_size != 0 else _ee_repr
    )

    for cls in [ee.Element, ee.ComputedObject]:
        _attach_html_repr(cls, rep)

    return rep


def clear_cache() -> None:
    """Reset the cache."""
    try:
        ee.Element._repr_html_.cache_clear()
    except AttributeError:
        pass
