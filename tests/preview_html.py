import tempfile
import webbrowser

import ee

from eerepr.repr import _repr_html_


def preview_html_output():
    from tests.test_html import get_test_objects

    objects = get_test_objects().items()

    rendered = _repr_html_(ee.List([obj[1] for obj in objects]))

    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(rendered)
        webbrowser.open(f.name)
    print(f"Rendered HTML output to {f.name}")


if __name__ == "__main__":
    ee.Initialize()
    preview_html_output()
