# SFSymbol Installation Guide

This package ships **two library products** from the same repository. Pick whichever API style you prefer:

- **`SFSymbol`** — flat enum, underscore names: `SFSymbol.star_fill.image`
- **`SFSymbolKit`** — strict, dot-notation: `SFSymbol.star.fill.image`

Both are kept up to date with the latest SF Symbols release (currently 7.2). Pick one per target — they should not be imported into the same Swift file.

## Prerequisites

- Xcode 15 or later (Swift 5.9+).
- Minimum deployment targets: iOS 13, macOS 11, watchOS 6, tvOS 13.

## Adding the package via Xcode

1. **Open your Xcode project**.
2. **File → Add Package Dependencies…**
3. Enter the repository URL:
   ```
   https://github.com/LuckeyLogic/SFSymbol.git
   ```
4. Pick a version rule (e.g. **Up to Next Major** from `2.0.0`) and click **Add Package**.
5. In the **Choose Package Products** sheet, check **one** of:
   - `SFSymbol` (legacy, underscore API), or
   - `SFSymbolKit` (new, dot-notation API)
6. Click **Add Package**.

If you're migrating an existing app from the old API, see [Migration.md](Migration.md).

## Adding the package via `Package.swift`

```swift
let package = Package(
    name: "MyApp",
    dependencies: [
        .package(url: "https://github.com/LuckeyLogic/SFSymbol", from: "2.0.0"),
    ],
    targets: [
        .target(name: "MyApp", dependencies: [
            // Pick ONE of these:
            .product(name: "SFSymbol",    package: "SFSymbol"),  // legacy
            .product(name: "SFSymbolKit", package: "SFSymbol"),  // new
        ]),
    ]
)
```

## Importing and using

### Legacy API (`SFSymbol`)

```swift
import SFSymbol

let starImage = SFSymbol.star_fill.image
```

### New API (`SFSymbolKit`)

```swift
import SFSymbolKit

let starImage = SFSymbol.star.fill.image
```

## Updating

To pull a newer version of the package, in Xcode: **File → Packages → Update to Latest Package Versions**. Or in `Package.swift`, run `swift package update`.

For the package maintainer regenerating against a new SF Symbols release, see the [README](../README.md#updating-to-a-new-sf-symbols-release).

## Troubleshooting

- **"No such module 'SFSymbol'"** — make sure you ticked the right product (or both, but in different files) in the Choose Package Products sheet.
- **`Image(systemName:)` warning on macOS 10.15** — this package requires macOS 11 because SwiftUI's `Image(systemName:)` initializer is only available from macOS 11.0.
- **Symbol not found at runtime (renders blank)** — confirm the SF Symbol name in the SF Symbols app and that your deployment target meets the symbol's `@available` requirement (only `SFSymbolKit` flags this at compile time).

If you hit something else, open an issue at <https://github.com/LuckeyLogic/SFSymbol/issues>.
