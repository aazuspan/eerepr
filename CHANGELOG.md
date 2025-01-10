# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Breaking Changes

- `eerepr` no longer initializes on import, and **must be manually initialized** to work.

    ```python
    import eerepr

    eerepr.initialize()
    ```

    If you're using `eerepr` through `geemap>=0.35.2`, this is [handled automatically](https://github.com/gee-community/geemap/pull/2183) by `geemap`.
- For security, HTML within Earth Engine objects is no longer rendered. This is consistent with the Code Editor.

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

[unreleased]: https://github.com/aazuspan/eerepr/compare/v0.0.4...HEAD
[0.0.4]: https://github.com/aazuspan/eerepr/compare/v0.0.3...v0.0.4
[0.0.3]: https://github.com/aazuspan/eerepr/compare/v0.0.2...v0.0.3
[0.0.2]: https://github.com/aazuspan/eerepr/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/aazuspan/eerepr/releases/tag/v0.0.1
