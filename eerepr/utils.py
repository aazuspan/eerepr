from functools import lru_cache
from importlib.resources import read_text


def is_nondeterministic(obj):
    """Check if an object returns nondeterministic results which would break caching.

    Currently, this only tests for the case of `ee.List.shuffle(seed=False)`.
    """
    invocation = obj.serialize()
    shuffled = "List.shuffle" in invocation
    false_seed = '"seed": {"constantValue": false}' in invocation
    return shuffled and false_seed


@lru_cache(maxsize=None)
def load_css():
    return read_text("eerepr.static.css", "style.css")


@lru_cache(maxsize=None)
def load_js():
    return read_text("eerepr.static.js", "widget.js")
