<p align="center">
  <img src="LuckeyLogicLogo1.png" alt="Logo" width="200"/>
</p>

# SFSymbol

SFSymbol is a Swift package that simplifies access to Apple's SF Symbols library, offering type-safe and dot-notation access to a wide range of icons for iOS, macOS, watchOS, and tvOS development. Enhance your app's user interface with ease.

## Introduction

Apple introduced SF Symbols as a way to provide developers with a comprehensive set of symbols for use in their applications. However, working with these symbols in code can be cumbersome due to the need to remember specific names and ensuring they match correctly.

SFSymbol makes working with SF Symbols more straightforward and less error-prone by providing an easy-to-use Swift enum that includes all available symbols. You can access symbols using a simple dot-notation syntax, making it intuitive and type-safe.

## Features

- **Type-Safe**: SFSymbol provides a type-safe way to access SF Symbols, preventing typos and compile-time errors in your code.

- **Dot Notation**: Access symbols using dot notation for improved readability and discoverability.

- **Comprehensive**: Includes a wide range of SF Symbols covering various categories, ensuring you have the right symbol for your needs.

- **Cross-Platform**: Compatible with iOS, macOS, watchOS, and tvOS projects.

- **Customization**: Easily customize symbols with modifiers like `.image`, `.font`, `.foregroundColor`, and more.

## Usage

Using SFSymbol in your project is straightforward:

1. Add SFSymbol as a Swift package dependency.
2. Import the SFSymbol module.
3. Access SF Symbols using dot notation, e.g., `SFSymbol.star_fill.image`.

```swift
import SFSymbol

let starImage = SFSymbol.star_fill.image
```

For more advanced usage and customization, refer to the [Documentation](#documentation) section.

## Installation

You can add SFSymbol to your project via Swift Package Manager or manually. Refer to the [Installation Guide](Documentation/Installation.md) for detailed instructions.

## Documentation

For detailed information on using SFSymbol, including customization options and advanced usage, please refer to the [Documentation](Documentation/Usage.md).

## License

SFSymbol is available under the [MIT License](LICENSE). You are free to use this package in your applications, even for commercial purposes, without open-sourcing your entire application. Please see the [License](LICENSE) file for more information.

## Contributions

Contributions to SFSymbol are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request. Please refer to the [Contribution Guide](CONTRIBUTING.md) for detailed instructions.

## Connect with Luckey Logic

Stay updated and connect with us on our website and social media platforms:

- Website: [Luckey Logic](https://luckeylogic.com/)
- [Instagram](https://www.instagram.com/luckeylogic)
- [Facebook](https://www.facebook.com/luckeylogic)
- [TikTok](https://www.tiktok.com/@luckeylogic)
- [YouTube](https://www.youtube.com/channel/UCYpu2dcEZ6VRi_DZtKV34ZQ)
- [LinkedIn](https://www.linkedin.com/company/luckeylogic)

Follow us for the latest updates, insights, and more.
