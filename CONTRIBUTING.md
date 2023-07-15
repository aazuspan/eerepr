# Contributing to eeprepr

Contributions are always welcome! Bugs and feature requests can be opened in the [Issues](https://github.com/aazuspan/eerepr/issues). Questions and comments can be posted in the [Discussions](https://github.com/aazuspan/eerepr/discussions). To contribute code, please open an issue to discuss implementation, then follow the guide below to get started!

## Setup

`eeprepr` uses [Hatch](https://hatch.pypa.io/latest/) for package and environment management. To set up a development environment, first fork and clone `eerepr`, then install `hatch` in your environment.

```bash
pip install hatch
```

This will install all required dependencies for development. You can enter the environment using:

```bash
hatch shell
```

and exit by typing `quit` or `CTRL + D`.

## Pre-commit Hooks

Pre-commit hooks automatically run linting, formatting, and type-checking whenever a change is commited. This ensures that the codebase is always in good shape.

The command below registers the pre-commit hooks for the project so that they run before every commit.

```bash
hatch run pre-commit install
```

To run all the checks manually, you can use:

```bash
hatch run pre-commit run --all-files
```

## Testing

### Running Tests

You can run all tests with `pytest` using the command below:

```bash
hatch run test:all
```

To measure test coverage, run:

```bash
hatch run test:cov
```

Additional arguments can be passed to `pytest` after the script name, e.g.:

```bash
hatch run test:all -k feature
```

### Building New Tests

New features should have unit tests. To avoid having to use `getInfo` every time a test is run against a client-side Earth Engine object, `eerepr` uses a caching function `tests.test_html.load_info` to load data. This function takes an Earth Engine object and either 1) retrieves it from the local cache in `tests/data/data.json` if it has been used before, or 2) retrieves it from the server and adds it to the cache. Objects in the cache use their serialized form as an identifying key.

To demonstrate, let's write a new dummy test that uses a custom `ee.Image`.

```python
from tests.test_html import load_info

def test_my_image():
    img = ee.Image.constant(42).set("custom_property", ["a", "b", "c"])
    info = load_info(img)

    assert info
```

The first time the test is run, `getInfo` will be used to retrieve the image metadata and store it in `tests/data/data.json`. Subsequent runs will pull the data directly from the cache.

When you add a new test, be sure to commit the updated data cache.