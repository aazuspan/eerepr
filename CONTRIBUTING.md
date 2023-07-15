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

New features should have unit tests. If your test needs to use `getInfo` to retrieve data from an Earth Engine object, you'll need to use the caching system described below.

Using `getInfo` to retrieve data from an Earth Engine object can be slow and network-dependent. To speed up tests, `eerepr` uses a caching function `tests.cache.get_info` to load data. This function takes an Earth Engine object and either 1) retrieves its info from a local cache file if it has been used before, or 2) retrieves it from the server and adds it to the cache. The cache directory and file (`tests/data/data.json`) will be created automatically the first time tests are run.

To demonstrate, let's write a new dummy test that checks the properties of a custom `ee.Image`.

```python
from tests.cache import get_info

def test_my_image():
    img = ee.Image.constant(42).set("custom_property", ["a", "b", "c"])
    # Use `get_info` instead of `img.getInfo` to utilize the cache
    info = get_info(img)

    assert "custom_property" in info["properties"]
```

The first time the test is run, `getInfo` will be used to retrieve the image metadata and store it in `tests/data/data.json`. Subsequent runs will pull the data directly from the cache.

Caches are kept locally and are not version-controlled, so there's no need to commit newly added objects.