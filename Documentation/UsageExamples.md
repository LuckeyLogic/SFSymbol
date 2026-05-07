# Usage Examples

Examples of using both library products. Pick whichever matches your import.

## Creating an Image

### `SFSymbolKit` (dot-notation)

```swift
import SwiftUI
import SFSymbolKit

struct ContentView: View {
    var body: some View {
        SFSymbol.star.fill.image
            .resizable()
            .scaledToFit()
            .foregroundColor(.blue)
            .frame(width: 50, height: 50)
    }
}
```

### `SFSymbol` (legacy underscore)

```swift
import SwiftUI
import SFSymbol

struct ContentView: View {
    var body: some View {
        SFSymbol.star_fill.image
            .resizable()
            .scaledToFit()
            .foregroundColor(.blue)
            .frame(width: 50, height: 50)
    }
}
```

## Customizing color

```swift
SFSymbol.heart.fill.image                 // SFSymbolKit
    .foregroundStyle(.red)

SFSymbol.heart_fill.image                 // SFSymbol (legacy)
    .foregroundStyle(.red)
```

## Multi-component paths

`SFSymbolKit` reads exactly like the SF Symbols app:

```swift
SFSymbol.square.and.arrow.up.image                          // "square.and.arrow.up"
SFSymbol.square.and.arrow.up.fill.image                     // "square.and.arrow.up.fill"
SFSymbol.person.crop.circle.badge.checkmark.image           // "person.crop.circle.badge.checkmark"
```

The legacy equivalents:

```swift
SFSymbol.square_and_arrow_up.image
SFSymbol.square_and_arrow_up_fill.image
SFSymbol.person_crop_circle_badge_checkmark.image
```

## Reading the symbol name (e.g. for UIKit/AppKit interop)

```swift
let name: String = SFSymbol.bell.fill.name              // SFSymbolKit  -> "bell.fill"
let name: String = SFSymbol.bell_fill.description       // SFSymbol     -> "bell.fill"

UIImage(systemName: name)
```

## Edge cases

```swift
// Leading digit
SFSymbol._4k.tv.image           // SFSymbolKit
SFSymbol._4k_tv.image           // SFSymbol

// Swift keyword
SFSymbol.`repeat`.image         // SFSymbolKit
SFSymbol._repeat.image          // SFSymbol

// "doc.text.image" — separate symbol distinct from "doc.text"
SFSymbol.doc.text.image_.image  // SFSymbolKit  -> Image for "doc.text.image"
SFSymbol.doc_text_image.image   // SFSymbol     -> same
```

## Compile-time availability (`SFSymbolKit` only)

Symbols introduced in SF Symbols 6 / 7 are gated to iOS 18 / iOS 19 respectively. If your deployment target is too low, the compiler tells you:

```swift
@available(iOS 18.0, *)
func newSymbol() -> Image {
    SFSymbol.apple.image.playground.image      // OK on iOS 18+
}
```

The legacy `SFSymbol` enum is annotated only at the type level (`iOS 13.0+`), so newer symbols compile but render blank on older OS versions.

## More

- [Installation](Installation.md)
- [Usage](Usage.md)
- [Migration guide (legacy → SFSymbolKit)](Migration.md)
