
# SFSymbol Documentation

Welcome to the SFSymbol documentation. This guide provides detailed information on using SFSymbol, including customization options and advanced usage. SFSymbol simplifies access to Apple's SF Symbols library, offering type-safe and dot-notation access to a wide range of icons for iOS, macOS, watchOS, and tvOS development.

## Table of Contents

1. [Introduction](#introduction)
2. [Type-Safe Access](#type-safe-access)
3. [Dot Notation](#dot-notation)
4. [Comprehensive Icon Set](#comprehensive-icon-set)
5. [Cross-Platform Compatibility](#cross-platform-compatibility)
6. [Customization](#customization)
7. [Usage Examples](#usage-examples)

## Introduction

Apple introduced SF Symbols to provide developers with a comprehensive set of symbols for use in their applications. However, working with these symbols in code can be cumbersome due to the need to remember specific names and ensuring they match correctly.

SFSymbol makes working with SF Symbols more straightforward and less error-prone by providing an easy-to-use Swift enum that includes all available symbols. You can access symbols using a simple dot-notation syntax, making it intuitive and type-safe.

## Type-Safe Access

SFSymbol provides a type-safe way to access SF Symbols, preventing typos and compile-time errors in your code. This ensures that you always use valid symbol names.

```swift
let starImage = SFSymbol.star_fill.image
```

## Dot Notation

Access symbols using dot notation for improved readability and discoverability. This allows you to quickly identify and use the symbols you need.

```swift
let heartImage = SFSymbol.heart_fill.image
```

## Comprehensive Icon Set

SFSymbol includes a wide range of SF Symbols covering various categories, ensuring you have the right symbol for your needs. Explore the extensive icon set to find the perfect symbol for your app.

## Cross-Platform Compatibility

SFSymbol is compatible with iOS, macOS, watchOS, and tvOS projects, making it versatile for multi-platform development.

## Customization

You can easily customize symbols with modifiers like `.image`, `.font`, `.foregroundColor`, and more. Tailor symbols to match your app's design and style.

```swift
let customImage = SFSymbol.star_fill
    .image
    .resizable()
    .scaledToFit()
    .foregroundColor(.blue)
```

## Usage Examples

For usage examples and code snippets, please refer to the [Usage Examples](Documentation/UsageExamples.md) section.

For any questions, issues, or suggestions, don't hesitate to reach out on the [SFSymbol GitHub repository](https://github.com/LuckeyLogic/SFSymbol). Happy coding!
