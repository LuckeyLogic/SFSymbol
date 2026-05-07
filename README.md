<p align="center">
  <img src="LuckeyLogicLogo1.png" alt="Logo" width="200"/>
</p>

# SFSymbol

[![Swift](https://img.shields.io/endpoint?url=https%3A%2F%2Fswiftpackageindex.com%2Fapi%2Fpackages%2FLuckeyLogic%2FSFSymbol%2Fbadge%3Ftype%3Dswift-versions)](https://swiftpackageindex.com/LuckeyLogic/SFSymbol)
[![Platforms](https://img.shields.io/endpoint?url=https%3A%2F%2Fswiftpackageindex.com%2Fapi%2Fpackages%2FLuckeyLogic%2FSFSymbol%2Fbadge%3Ftype%3Dplatforms)](https://swiftpackageindex.com/LuckeyLogic/SFSymbol)
[![License](https://img.shields.io/github/license/LuckeyLogic/SFSymbol)](LICENSE)

Type-safe access to Apple's SF Symbols catalog from Swift, for iOS, macOS, watchOS, and tvOS. Two flavors:

- **`SFSymbol`** — flat enum with underscore-style names: `SFSymbol.star_fill.image`
- **`SFSymbolKit`** — strict, nested dot-notation API: `SFSymbol.star.fill.image`

Both are generated from Apple's catalog (currently **SF Symbols 7.2**) by the same script, so they stay in lock-step on every Apple release.

## Pick one

```swift
// Package.swift
.package(url: "https://github.com/LuckeyLogic/SFSymbol", from: "2.0.0"),

// Then add ONE of these to your target's dependencies:
.product(name: "SFSymbol",    package: "SFSymbol"),  // legacy underscore API
.product(name: "SFSymbolKit", package: "SFSymbol"),  // new dot-notation API
```

### `SFSymbol` (legacy, underscore)

```swift
import SFSymbol

let starImage:  Image  = SFSymbol.star_fill.image
let arrowImage: Image  = SFSymbol.square_and_arrow_up.image
let name:       String = SFSymbol.heart_fill.description  // "heart.fill"
```

### `SFSymbolKit` (new, dot-notation)

```swift
import SFSymbolKit

let starImage:  Image  = SFSymbol.star.fill.image
let arrowImage: Image  = SFSymbol.square.and.arrow.up.image
let name:       String = SFSymbol.heart.fill.name         // "heart.fill"
```

The dot-notation API gives you:

- **Type-safe combinations** — `SFSymbol.star.bogus` won't compile.
- **Per-symbol availability** — `@available` is annotated per symbol, so the compiler tells you when a SF Symbols 6/7 symbol isn't available on your deployment target.
- **Narrower autocomplete** — typing `SFSymbol.star.` only shows valid `star.*` continuations.

See [Documentation/Migration.md](Documentation/Migration.md) for a full mapping between the two APIs and the three small escape rules (leading-digit segments, Swift keywords, the `doc.text.image` collision).

## Why both?

Existing apps using the legacy `SFSymbol` keep working — no breaking changes. The new `SFSymbolKit` is opt-in via a separate Swift module, so the underscore names never bleed into the new namespace and vice versa.

Both are regenerated from Apple's `name_availability.plist` on every SF Symbols release; maintaining both has zero marginal cost.

## Updating to a new SF Symbols release

```bash
python3 Tools/generate.py
swift test
```

The script reads `/Applications/SF Symbols.app/Contents/Resources/Metadata/name_availability.plist` and rewrites both libraries.

## Installation

See [Documentation/Installation.md](Documentation/Installation.md).

## Documentation

- [Usage](Documentation/Usage.md)
- [Examples](Documentation/UsageExamples.md)
- [Migration guide (legacy → SFSymbolKit)](Documentation/Migration.md)

## License

MIT — see [LICENSE](LICENSE).

## Contributions

Issues and PRs welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Connect with Luckey Logic

- Website: [luckeylogic.com](https://luckeylogic.com/)
- [Instagram](https://www.instagram.com/luckeylogic)
- [Facebook](https://www.facebook.com/luckeylogic)
- [TikTok](https://www.tiktok.com/@luckeylogic)
- [YouTube](https://www.youtube.com/channel/UCYpu2dcEZ6VRi_DZtKV34ZQ)
- [LinkedIn](https://www.linkedin.com/company/luckeylogic)
