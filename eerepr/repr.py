from __future__ import annotations

import html
import uuid
from functools import _lru_cache_wrapper, lru_cache
from typing import Any, Literal, Union
from warnings import warn

import ee

from eerepr.config import Config
from eerepr.html import convert_to_html, escape_object
from eerepr.style import CSS

REPR_HTML = "_repr_html_"
EEObject = Union[ee.Element, ee.ComputedObject]

# Track which repr methods have been set so we can overwrite them if needed.
reprs_set: set[EEObject] = set()
options = Config()


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
    # Escape all strings in object info to prevent injection
    info = escape_object(obj.getInfo())
    body = convert_to_html(info)

    return (
        "<div>"
        f"<style>{CSS}</style>"
        "<div class='eerepr'>"
        f"<ul>{body}</ul>"
        "</div>"
        "</div>"
    )


def _ee_repr(obj: EEObject) -> str:
    """Wrapper around _repr_html_ to prevent cache hits on nondeterministic objects."""
    if _is_nondeterministic(obj):
        # We don't want to cache nondeterministic objects, so we'll add add a unique
        # attribute that causes ee.ComputedObject.__eq__ to return False, preventing a
        # cache hit.
        obj._eerepr_id = uuid.uuid4()

    try:
        rep = _repr_html_(obj)
    except ee.EEException as e:
        if options.on_error == "raise":
            raise e from None

        warn(
            f"Getting info failed with: '{e}'. Falling back to string repr.",
            stacklevel=2,
        )
        return f"<pre>{html.escape(repr(obj))}</pre>"

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
    """Attach HTML repr methods to EE objects and set the cache size.

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
    global _repr_html_
    options.update(
        max_cache_size=max_cache_size,
        max_repr_mbs=max_repr_mbs,
        on_error=on_error,
    )

    if isinstance(_repr_html_, _lru_cache_wrapper):
        _repr_html_ = _repr_html_.__wrapped__  # type: ignore

    if max_cache_size != 0:
        _repr_html_ = lru_cache(maxsize=options.max_cache_size)(_repr_html_)

    for cls in [ee.Element, ee.ComputedObject]:
        _attach_html_repr(cls, _ee_repr)


def reset():
    """Remove HTML repr methods added by eerepr to EE objects."""
    for cls in reprs_set:
        if hasattr(cls, REPR_HTML):
            delattr(cls, REPR_HTML)
