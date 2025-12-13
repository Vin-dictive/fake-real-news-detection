# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Updated Makefile to run tests after data download in pipeline
- Renamed test files to follow pytest naming conventions (underscores instead of hyphens)

## [562d91b] - 2024-12-XX - Peer review feedback

**Issue:** [#41](https://github.com/Vin-dictive/fake-real-news-detection/issues/41)

### Changed

- Removed one of the word cloud images based on peer review feedback
- Updated README to keep only 1 image of the word cloud
- Converted README analysis options to accordion format for better organization
- Added Docker as a dependency in README

### Improved

- Enhanced README readability with collapsible sections
- Better documentation structure for setup options

## [ea1ee45] - 2024-12-XX - Peer review feedback

**Issue:** [#41](https://github.com/Vin-dictive/fake-real-news-detection/issues/41)

### Fixed

- Fixed Makefile issue that was not running all scripts sequentially
- Makefile now properly executes complete pipeline instead of only report script dependencies
- Added test functions to Makefile to address Quarto render reliability issues

### Added

- Comprehensive test integration in build pipeline
- Better error handling for pipeline execution

## [92dfcef] - 2024-12-XX - Peer review feedback

**Issue:** [#41](https://github.com/Vin-dictive/fake-real-news-detection/issues/41)

### Added

- Added specific version numbers for all dependencies in environment.yml file
- Improved reproducibility with locked dependency versions

### Changed

- Updated environment configuration for better consistency across different systems
