from __future__ import annotations

import uuid
from functools import _lru_cache_wrapper, lru_cache
from html import escape
from typing import Any, Union
from warnings import warn

import ee

from eerepr.config import options
from eerepr.html import convert_to_html

REPR_HTML = "_repr_html_"
EEObject = Union[ee.Element, ee.ComputedObject]

# Track which repr methods have been set so we can overwrite them if needed.
reprs_set: set[EEObject] = set()


def _load_file(package: str, resource: str) -> str:
    """
    Compatibility wrapper for deprecated `importlib.resources.read_text`.

    Replace with `importlib.resources.files` once support for Python < 3.9 is dropped.
    """
    try:
        # Python >= 3.9
        from importlib.resources import files

        return files(package).joinpath(resource).read_text()
    except ImportError:
        from importlib.resources import read_text

        return read_text(package, resource)


@lru_cache(maxsize=1)
def _load_css() -> str:
    return _load_file("eerepr.static.css", "style.css")


@lru_cache(maxsize=1)
def _load_js() -> str:
    """Note: JS is only needed because the CSS `:has()` selector isn't well supported
    yet, preventing a pure CSS solution to the collapsible lists.
    """
    return _load_file("eerepr.static.js", "script.js")


def _attach_html_repr(cls: type, repr: Any) -> None:
    """Add a HTML repr method to an EE class. Only overwrite the method if it was set by
    this function.
    """
    if not hasattr(cls, REPR_HTML) or cls in reprs_set:
        reprs_set.update([cls])
        setattr(cls, REPR_HTML, repr)


def _is_nondeterministic(obj: EEObject) -> bool:
    """Check if an object returns nondeterministic results which would break caching.

    Currently, this only tests for the case of `ee.List.shuffle(seed=False)`.
    """
    invocation = obj.serialize()
    shuffled = "List.shuffle" in invocation
    false_seed = '"seed": {"constantValue": false}' in invocation
    return shuffled and false_seed


@lru_cache(maxsize=None)
def _repr_html_(obj: EEObject) -> str:
    """Generate an HTML representation of an EE object."""
    try:
        info = obj.getInfo()
    # Fall back to a string repr if getInfo fails
    except ee.EEException as e:
        warn(
            f"Getting info failed with: '{e}'. Falling back to string repr.",
            stacklevel=2,
        )
        return f"<pre>{escape(repr(obj))}</pre>"

    css = _load_css()
    js = _load_js()
    body = convert_to_html(info)

    return (
        "<div>"
        f"<style>{css}</style>"
        "<div class='ee'>"
        f"<ul>{body}</ul>"
        "</div>"
        f"<script>{js}</script>"
        "</div>"
    )


def _ee_repr(obj: EEObject) -> str:
    """Wrapper around _repr_html_ to prevent cache hits on nondeterministic objects."""
    if _is_nondeterministic(obj):
        # We don't want to cache nondeterministic objects, so we'll add add a unique
        # attribute that causes ee.ComputedObject.__eq__ to return False, preventing a
        # cache hit.
        obj._eerepr_id = uuid.uuid4()

    rep = _repr_html_(obj)
    mbs = len(rep) / 1e6
    if mbs > options.max_repr_mbs:
        warn(
            message=(
                f"HTML repr size ({mbs:.0f}mB) exceeds maximum"
                f" ({options.max_repr_mbs:.0f}mB), falling back to string repr. You"
                " can set `eerepr.options.max_repr_mbs` to print larger objects,"
                " but this may cause performance issues."
            ),
            stacklevel=2,
        )
        return f"<pre>{escape(repr(obj))}</pre>"

    return rep


def initialize(max_cache_size: int | None = None) -> None:
    """Attach HTML repr methods to EE objects and set the cache size.

    Re-running this function will reset the cache.

    Parameters
    ----------
    max_cache_size : int, optional
        The maximum number of EE objects to cache. If None, the cache size is unlimited.
        Set to 0 to disable caching.
    """
    global _repr_html_
    if isinstance(_repr_html_, _lru_cache_wrapper):
        _repr_html_ = _repr_html_.__wrapped__  # type: ignore

    if max_cache_size != 0:
        _repr_html_ = lru_cache(maxsize=max_cache_size)(_repr_html_)

    for cls in [ee.Element, ee.ComputedObject]:
        _attach_html_repr(cls, _ee_repr)


def reset():
    """Remove HTML repr methods added by eerepr to EE objects."""
    for cls in reprs_set:
        delattr(cls, REPR_HTML)
