// swift-tools-version: 5.9
// The swift-tools-version declares the minimum version of Swift required to build this package.

import PackageDescription

let package = Package(
    name: "SFSymbol",
    platforms: [
        .iOS(.v13),
        .macOS(.v11),
        .watchOS(.v6),
        .tvOS(.v13),
    ],
    products: [
        // Legacy underscore API: `SFSymbol.star_fill.image`.
        .library(name: "SFSymbol", targets: ["SFSymbol"]),
        // Type-safe dot-notation API: `SFSymbol.star.fill.image`.
        .library(name: "SFSymbolKit", targets: ["SFSymbolKit"]),
    ],
    targets: [
        .target(name: "SFSymbol", path: "Sources/SFSymbol"),
        .target(name: "SFSymbolKit", path: "Sources/SFSymbolKit"),
        .testTarget(
            name: "SFSymbolTests",
            dependencies: ["SFSymbol", "SFSymbolKit"],
            path: "Tests/SFSymbolTests"
        ),
    ]
)
