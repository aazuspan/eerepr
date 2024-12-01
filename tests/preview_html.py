import webbrowser

import ee

from eerepr.repr import _repr_html_
from tests.conftest import CACHE_DIR


def preview_html_output():
    from tests.test_html import get_test_objects

    objects = get_test_objects().items()

    rendered = _repr_html_(ee.List([obj[1] for obj in objects]))

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    preview_path = CACHE_DIR / ".preview.html"
    with open(preview_path, "w") as f:
        f.write(rendered)

    webbrowser.open(f"file://{preview_path}")
    print(f"Rendered HTML output to {preview_path}")


if __name__ == "__main__":
    ee.Initialize()
    preview_html_output()
