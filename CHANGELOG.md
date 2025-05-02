# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

## [0.1.2] - 2025-05-02

### Changed

- `eerepr.reset()` now clears the cache immediately instead of waiting for `eerepr.initialize()`.

### Performance

- Non-deterministic objects are no longer cached, rather than getting a unique attribute to force a cache miss. Negligible reduction in memory, unless you're caching huge shuffled lists.
- The optimization of long truncated lists was modified to check list lengths against a pre-computed max length instead of calculating the minimum string length of each list. Minor speedup when working with a lot of lists.

## [0.1.1] - 2025-02-19

### Fixed

- Fixed an error generating reprs when the default system encoding is `gbk`

### Performance

- Avoid stringifying long lists that will definitely be truncated in the repr (~20% speedup when testing with a 25-image Sentinel-2 collection)

### Changed

- CSS is loaded from a Python module instead of a static file

## [0.1.0] - 2025-01-10

### Breaking Changes

- `eerepr` no longer initializes on import, and **must be manually initialized** to work.

    ```python
    import eerepr

    eerepr.initialize()
    ```

    If you're using `eerepr` through `geemap>=0.35.2`, this is [handled automatically](https://github.com/gee-community/geemap/pull/2183) by `geemap`.

### Added

- Add `on_error` parameter to `initialize` with option `raise` to throw Earth Engine exceptions instead of warning
- Add `max_repr_mbs` parameter to `initialize` to allow setting the maximum repr size for safety

### Changed

- Pure CSS collapsing (no more JS!)
- Better accessibility - reprs can be navigated by keyboard
- Optimized dict sorting (3-10% faster)
- Improved styling

### Fixed

- Replaced deprecated standard lib functions

### Removed

- Dropped Python 3.7 support
- Automatic `initialize` on import

## [0.0.5] - 2025-01-19

This release is a backport of a security fix from `0.1.0`.

### Breaking Changes

- For security, HTML within Earth Engine objects is no longer rendered. This is consistent with the Code Editor.

### Security

- Escape HTML in all server-side data to prevent injection attacks

## [0.0.4] - 2022-11-30

### Added

- Added Python 3.7 support

### Fixed

- Fixed null geometry feature reprs

## [0.0.3] - 2022-11-26

### Added

- Available on [conda-forge](https://anaconda.org/conda-forge/eerepr)

### Changed

- Reduced repr storage size by 30%

## [0.0.2] - 2022-11-09

### Added

- New `config` module to control caching and repr size limits

### Changed

- Prevent printing huge reprs

### Fixed

- Fixed caching bug on `ee.List.shuffle(seed=False)`
- Fixed collapsing duplicate objects in Jupyter Lab

## [0.0.1] - 2022-11-06

### Added

- Initial release

---

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

[unreleased]: https://github.com/aazuspan/eerepr/compare/v0.1.2...HEAD
[0.1.2]: https://github.com/aazuspan/eerepr/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/aazuspan/eerepr/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/aazuspan/eerepr/compare/v0.0.4...v0.1.0
[0.0.5]: https://github.com/aazuspan/eerepr/compare/v0.0.4...v0.0.5
[0.0.4]: https://github.com/aazuspan/eerepr/compare/v0.0.3...v0.0.4
[0.0.3]: https://github.com/aazuspan/eerepr/compare/v0.0.2...v0.0.3
[0.0.2]: https://github.com/aazuspan/eerepr/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/aazuspan/eerepr/releases/tag/v0.0.1
