# SFSymbol Usage

This package gives you type-safe access to Apple's full SF Symbols catalog (currently 7.2, ~7,800 symbols) from Swift. Two library products are available; pick one per target:

| Product | Style | Example |
|---|---|---|
| `SFSymbol`    | Flat enum, underscore names | `SFSymbol.star_fill.image` |
| `SFSymbolKit` | Strict, dot-notation         | `SFSymbol.star.fill.image` |

Both expose a SwiftUI `Image` and a `String` for the symbol name. Both are generated from Apple's catalog and updated in lock-step on every SF Symbols release.

## Type safety

### Legacy `SFSymbol`

Each symbol is an enum case. Typos won't compile:

```swift
SFSymbol.star_fill.image    // ✅ valid
SFSymbol.starr_fill.image   // ❌ compile error
```

`@available(iOS 13.0, *)` is declared once on the enum. Symbols introduced in newer SF Symbols releases will compile on iOS 13 but render blank at runtime.

### New `SFSymbolKit`

Each symbol path is a chain of nested namespaces. Invalid combinations don't compile, *and* per-symbol availability is enforced at compile time:

```swift
SFSymbol.star.fill.image                 // ✅ valid
SFSymbol.star.bogus.fill.image           // ❌ compile error
SFSymbol.apple.image.playground.image    // ❌ compile error if you target iOS 17 — symbol is iOS 18+
```

If your deployment target is too low for a symbol, the compiler tells you instead of letting it ship and silently render blank.

## Reading the symbol name

```swift
// Legacy
let s: String = SFSymbol.heart_fill.description   // "heart.fill"

// SFSymbolKit
let s: String = SFSymbol.heart.fill.name          // "heart.fill"
```

The legacy enum conforms to `RawRepresentable` (`String`) and `CustomStringConvertible`. `SFSymbolKit` does not — it uses caseless enums for namespacing, which can't be values, so it exposes static `name` and `image` accessors at each leaf instead.

## Customization

The `image` accessor returns a SwiftUI `Image`, so you can apply any standard SwiftUI modifier:

```swift
import SwiftUI
import SFSymbolKit  // or `import SFSymbol`

struct ContentView: View {
    var body: some View {
        SFSymbol.star.fill.image           // SFSymbolKit
            .resizable()
            .scaledToFit()
            .foregroundColor(.blue)
            .frame(width: 50, height: 50)
    }
}
```

For UIKit/AppKit, use the `name` (or `description` on the legacy enum) and pass it to `UIImage(systemName:)` / `NSImage(systemSymbolName:)` yourself.

## Escape rules (`SFSymbolKit` only)

Three small rules let Swift identifiers handle cases that don't map cleanly:

1. **Leading-digit segments → `_` prefix.** `4k.tv` → `SFSymbol._4k.tv`.
2. **Swift keyword segments → backticks.** `repeat` → `` SFSymbol.`repeat` ``. Same for `case`, `return`, `in`, `switch`, `open`, `extension`, `indirect`, `subscript`.
3. **`doc.text.image` collision → trailing underscore.** Both `doc.text` and `doc.text.image` are real symbols; the deeper one is reached as `SFSymbol.doc.text.image_`. This is the only such collision in the current catalog.

The legacy `SFSymbol` collapses all of these by replacing dots with underscores: `SFSymbol._4k_tv`, `SFSymbol._repeat`, `SFSymbol.doc_text_image`.

## More

- [Installation](Installation.md)
- [Usage examples](UsageExamples.md)
- [Migration guide (legacy → SFSymbolKit)](Migration.md)
