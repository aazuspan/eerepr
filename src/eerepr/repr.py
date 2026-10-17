from __future__ import annotations

import html
from functools import _lru_cache_wrapper, cache, lru_cache
from typing import Any, Literal
from warnings import warn

import ee

from eerepr.config import Config
from eerepr.html import _escape_str, build_html_repr

REPR_HTML = "_repr_html_"
EEObject = ee.Element | ee.ComputedObject

# Track which repr methods have been set so we can overwrite them if needed.
reprs_set: set[type[EEObject]] = set()
options = Config()


class _UncachedRepr(Exception):
    """A rendered HTML representation that was raised to escape the cache."""

    def __init__(self, html: str):
        self.html = html


def _repr_html_(obj: EEObject) -> str:
    """Generate an HTML representation of an EE object."""
    try:
        rep = _cached_repr(obj)
    except _UncachedRepr as uncached:
        rep = uncached.html
    except ee.EEException as exc:
        return _error_repr(obj=obj, exc=exc)
    return _limit_repr_size(rep=rep, obj=obj)


@cache
def _cached_repr(obj: EEObject) -> str:
    """Inner HTML generation for EE objects."""
    info = obj.getInfo()
    html_repr = build_html_repr(info)

    # Raise to force a cache miss for non-deterministic objects
    if _is_nondeterministic(obj):
        raise _UncachedRepr(html=html_repr)
    return html_repr


def _is_nondeterministic(obj: EEObject) -> bool:
    """Check if an object returns nondeterministic results which would break caching.

    Non-deterministic here means that the same client-side computation graph can produce
    different results on the server, making stale cache entries much more likely.
    Technically any computation that depends on server data could be non-deterministic,
    e.g. an image query can become stale as new assets are ingested; this check just
    focuses on data-independent non-determinism, which has only been observed in
    `ee.List.shuffle(seed=False)`.
    """
    invocation = obj.serialize()
    return (
        # Check the rarer `seed=False` condition first.
        '"seed": {"constantValue": false}' in invocation
        # Verify there is also a `List.shuffle` call. This could technically be a
        # false positive since we don't check the context of the `seed` argument, but
        # `List.shuffle` is the only function that currently supports a boolean `seed`.
        and "List.shuffle" in invocation
    )


def _error_repr(obj: EEObject, exc: ee.EEException) -> str:
    """Generate an HTML representation for an EE object that encountered an error."""
    if options.on_error == "raise":
        raise exc from None

    warn(
        f"Getting info failed with: '{exc}'. Falling back to string repr.",
        stacklevel=2,
    )
    return f"<pre>{html.escape(repr(obj))}</pre>"


def _limit_repr_size(rep: str, obj: EEObject) -> str:
    """Limit the size of the HTML representation, falling back to the string repr."""
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
        return f"<pre>{html.escape(repr(obj))}</pre>"

    return rep


def initialize(
    max_cache_size: int | None = None,
    max_repr_mbs: int = 100,
    on_error: Literal["warn", "raise"] = "warn",
) -> None:
    """Attach HTML repr methods to EE objects and initialize a cache.

    Re-running this function will reset the cache.

    Parameters
    ----------
    max_cache_size : int, optional
        The maximum number of EE objects to cache. If None, the cache size is unlimited.
        Set to 0 to disable caching.
    max_repr_mbs : int, default 100
        The maximum HTML repr size to display, in MBs. Setting this too high may freeze
        the client when printing very large objects. When a repr exceeds this size, the
        string repr will be displayed instead along with a warning.
    on_error : {'warn', 'raise'}, default 'warn'
        Whether to raise an error or display a warning when an error occurs fetching
        Earth Engine data.
    """
    global _cached_repr
    options.update(
        max_cache_size=max_cache_size,
        max_repr_mbs=max_repr_mbs,
        on_error=on_error,
    )

    if isinstance(_cached_repr, _lru_cache_wrapper):
        _cached_repr = _cached_repr.__wrapped__  # type: ignore

    if max_cache_size != 0:
        _cached_repr = lru_cache(maxsize=options.max_cache_size)(_cached_repr)

    for cls in [ee.Element, ee.ComputedObject]:
        _attach_html_repr(cls, _repr_html_)


def reset():
    """Remove HTML repr methods added by eerepr to EE objects and reset the cache."""
    for cls in reprs_set:
        if hasattr(cls, REPR_HTML):
            delattr(cls, REPR_HTML)

    reprs_set.clear()
    _escape_str.cache_clear()
    if isinstance(_cached_repr, _lru_cache_wrapper):
        _cached_repr.cache_clear()


def _attach_html_repr(cls: type, repr: Any) -> None:
    """Add a HTML repr method to an EE class. Only overwrite the method if it was set by
    this function.
    """
    if not hasattr(cls, REPR_HTML) or cls in reprs_set:
        reprs_set.update([cls])
        setattr(cls, REPR_HTML, repr)
