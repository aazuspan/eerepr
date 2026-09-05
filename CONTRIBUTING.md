# Contributing to eeprepr

Contributions are always welcome! Bugs and feature requests can be opened in the [Issues](https://github.com/aazuspan/eerepr/issues). Questions and comments can be posted in the [Discussions](https://github.com/aazuspan/eerepr/discussions). To contribute code, please open an issue to discuss implementation, then follow the guide below to get started!

## Developer tools

[uv](https://docs.astral.sh/uv/getting-started/installation/) is recommended for developer tooling. Fork and clone `eerepr`, then use `uv sync` to install a local virtual environment. The `pyproject.toml` defines a number of [poethepoet](https://poethepoet.natn.io/index.html) tasks for common development workflows, including:

```bash
poe lint
poe format
poe type-check
```

For convenience, runs all three commands above with:

```bash
poe check
```

## Testing

Run tests with:

```bash
poe test
```

### Regression Testing

Rendered HTML is tested using [pytest-regressions](https://pytest-regressions.readthedocs.io/en/latest/overview.html), which compares the current HTML output for each object to the previously recorded output (tracked in version control). Tests will fail if the HTML output changes. If the change is correct (i.e. an update to the HTML formatting or a difference in object representations in Earth Engine), use the `--force-regen` argument to regenerate a new "reference" HTML output, and commit the updated reference file.

### Local Object Cache

Tests that rely on server-side data via `getInfo` are slow, so `eerepr` uses a mocked `getInfo` method for all tests. When `getInfo` is run on a new object, the value is computed server-side and stored in the local cache file (`tests/data/.cache.json`). A warning is thrown to alert you. Subsequent calls to `getInfo` with the same object (based on its serialized form) will return data from the cache instead of Earth Engine servers. If the cache somehow becomes stale, i.e. the value returned by Earth Engine changes, you can manually delete the cache file and re-run tests to regenerate it. Caches are kept locally and are **not version-controlled**.

When a new object is added to regression testing, the first run will fail and generate a new reference file. Subsequent tests will pass. Output from regression testing **is version controlled**, so new outputs should be committed.

### Previewing HTML Output

Running the command below renders an HTML repr with a variety of different EE objects and opens it in the default web browser. Use this to visually compare results with outputs from the Code Editor.

```bash
poe preview
```