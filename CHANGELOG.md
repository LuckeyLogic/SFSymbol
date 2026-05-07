# Changelog

All notable changes to the `SFSymbol` project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.0] - 2026-05-07

### Added
- New `SFSymbolKit` library product — type-safe, dot-notation API: `SFSymbol.star.fill.image`. Uses nested caseless enums so only Apple-published variants are reachable; invalid combinations are compile errors.
- Per-symbol `@available` annotations in `SFSymbolKit`, so symbols introduced in newer SF Symbols releases are gated to the correct minimum OS version.
- `Tools/generate.py` — single source of truth that regenerates both libraries from `/Applications/SF Symbols.app/Contents/Resources/Metadata/name_availability.plist`. Run after any SF Symbols release.
- `Documentation/Migration.md` — guide for moving from the underscore API to `SFSymbolKit`.
- `Tests/SFSymbolTests/` — XCTest suite exercising both APIs, the keyword/digit escape rules, and the `doc.text.image` collision case.

### Changed
- `SFSymbol` updated from SF Symbols 5.0 to **7.2 (build 119)** — adds 2,420 new symbols. No existing case names removed; this is a pure superset.
- `Package.swift` now declares platforms (`iOS 13`, `macOS 11`, `watchOS 6`, `tvOS 13`). macOS minimum is 11 because `SwiftUI.Image(systemName:)` is macOS 11+.
- The `SFSymbol` enum is now generated; do not edit `Sources/SFSymbol/SFSymbol.swift` by hand.

## [1.1.0] - 2023-12-06

## [1.0.0] - 2023-12-05

### Added
- Initial release of the SFSymbol package, offering simplified access to SF Symbols with type safety and dot notation.

### Changed
                                          
### Deprecated
                                          
### Removed
                                          
### Fixed
                                          
### Security

## [1.0.1] - 2023-12-06

### Added

### Changed
- Updated `SFSymbol.swift` to make the enum and its members `public` for external access.
- Modified `Package.swift` to specify platforms and Swift version for broader compatibility.
                                          
### Deprecated
                                          
### Removed
                                          
### Fixed
                                          
### Security

## [1.1.0] - 2023-12-06

### Added
- Updated 9 new symbols to SFSybol library that were added by Apple
- Implemented a '.description' property for SFSymbol that returns the string of the symbol

### Changed
- None
                                          
### Deprecated
- None

### Removed
- None

### Fixed
- None

### Security
- None

> **Note:** Subsequent releases should follow the same structure, listing changes under respective versions and categories like 'Added', 'Changed', 'Deprecated', 'Removed', 'Fixed', and 'Security'.
