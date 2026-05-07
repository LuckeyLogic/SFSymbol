<p align="center">
  <img src="../LuckeyLogicLogo1.png" alt="Logo" width="200"/>
</p>

# Migrating from `SFSymbol` to `SFSymbolKit`

`SFSymbolKit` is a new library product in this Swift package that exposes Apple's SF Symbols catalog through a type-safe, dot-notation API. It ships alongside the original `SFSymbol` library — you choose one or the other in your `Package.swift`.

This guide explains the differences, why you might switch, and exactly what the rename rules are.

## TL;DR

```swift
// Legacy SFSymbol  (underscore-style, type-safe via enum cases)
import SFSymbol
let starImage = SFSymbol.star_fill.image

// New SFSymbolKit  (dot-notation, type-safe via nested namespaces)
import SFSymbolKit
let starImage = SFSymbol.star.fill.image
```

Both library products are generated from the same Apple catalog by `Tools/generate.py`, so they stay in lock-step on every SF Symbols release.

## Why `SFSymbolKit`

| | `SFSymbol` | `SFSymbolKit` |
|---|---|---|
| Lookup style | Flat enum cases (`SFSymbol.star_fill`) | Nested namespaces (`SFSymbol.star.fill`) |
| Path readability | Underscores between every component | Real dots, matches Apple's docs |
| Per-symbol availability | `@available(iOS 13, *)` on the whole enum | Per-symbol `@available(...)` annotations |
| Discoverability via autocomplete | Flat list of ~7,800 cases | Tree — only relevant variants surface as you type |
| Conforms to `RawRepresentable` | Yes (`String` raw values) | No — leaves expose `name: String` instead |

The big practical wins of `SFSymbolKit`:

1. **Autocomplete narrows as you type.** After `SFSymbol.star.`, Xcode shows only valid `star.*` continuations (`fill`, `circle`, `slash`, …) instead of the full 7,800-entry list.
2. **Compile-time availability checks.** If you target iOS 16 and reach for a SF Symbols 6 variant introduced in iOS 18, the compiler flags it, not your QA.
3. **Reads like Apple's documentation.** `SFSymbol.square.and.arrow.up.fill` matches the `square.and.arrow.up.fill` you see in the SF Symbols app.

## How to switch

### 1. Add the new product to your `Package.swift`

```swift
.package(url: "https://github.com/LuckeyLogic/SFSymbol", from: "2.0.0"),
```

In your target's dependencies, replace `"SFSymbol"` with `"SFSymbolKit"` (or add it alongside `"SFSymbol"` if you want a gradual migration):

```swift
.target(name: "MyApp", dependencies: [
    .product(name: "SFSymbolKit", package: "SFSymbol"),
])
```

### 2. Translate call sites

The translation rule is mechanical: replace each `_` with `.` and drop the leading underscore.

| Legacy | New |
|---|---|
| `SFSymbol.star.image` | `SFSymbol.star.image` |
| `SFSymbol.star_fill.image` | `SFSymbol.star.fill.image` |
| `SFSymbol.square_and_arrow_up.image` | `SFSymbol.square.and.arrow.up.image` |
| `SFSymbol.person_2_fill.image` | `SFSymbol.person._2.fill.image` |
| `SFSymbol._4k_tv.image` | `SFSymbol._4k.tv.image` |
| `SFSymbol._repeat.image` | ``SFSymbol.`repeat`.image`` |
| `SFSymbol._case.image` | ``SFSymbol.`case`.image`` |

### 3. Property changes

- Both expose `image: Image` and a string for the symbol name.
- The string accessor moved: legacy uses `description` (from `CustomStringConvertible`), `SFSymbolKit` uses `name`.

```swift
// before
let s: String = SFSymbol.star_fill.description

// after
let s: String = SFSymbol.star.fill.name
```

If you relied on `RawRepresentable` conformance (e.g. for `Codable`), stay on the legacy `SFSymbol` for those code paths.

## The escape rules

`SFSymbolKit` keeps Apple's symbol names exactly. Three small mangling rules apply because Swift identifiers can't start with a digit and certain words are reserved:

1. **Leading-digit segments → leading underscore.**
   `4k.tv` becomes `SFSymbol._4k.tv`. The underscore is *only* on the first segment, never as a separator.

2. **Swift keyword segments → backticks.**
   `repeat` is a Swift keyword, so the symbol named `repeat` becomes ``SFSymbol.`repeat` ``. Same for ``case``, ``return``, ``in``, ``switch``, ``open``, ``extension``, ``indirect``, ``subscript``.

3. **`.image` collision (one rare case).**
   Apple ships both `doc.text` and `doc.text.image` as separate symbols. Because `.image` is the leaf accessor we use to obtain the SwiftUI `Image`, the deeper symbol gets a trailing underscore in the dot path:

   ```swift
   SFSymbol.doc.text.image          // SwiftUI Image for "doc.text"
   SFSymbol.doc.text.image_.image   // SwiftUI Image for "doc.text.image"
   SFSymbol.doc.text.image_.fill.image
   ```

   This is the only such collision in the current catalog.

## Side-by-side coexistence

You can keep `SFSymbol` (legacy) and `SFSymbolKit` in the same target during a migration. They are separate Swift modules with no overlapping types — `import SFSymbol` and `import SFSymbolKit` give you two independent `SFSymbol` namespaces. If you need to refer to both from the same file, fully qualify:

```swift
import SFSymbol
import SFSymbolKit

let a = SFSymbol.star_fill.image           // legacy
let b = SFSymbolKit.SFSymbol.star.fill.image  // new
```

## Long-term plan

Both products are kept up to date by re-running `Tools/generate.py` against each new SF Symbols release. There is no plan to deprecate the legacy `SFSymbol` library — it remains supported for as long as the generator keeps producing it.

If you have feedback on the new API or hit a symbol that doesn't translate the way you expect, open an issue at <https://github.com/LuckeyLogic/SFSymbol/issues>.
