# Usage Examples

This section provides usage examples and code snippets to help you get started with SFSymbol in your projects. Below, you'll find examples of how to use SFSymbol for various tasks, such as creating images, setting colors, and customizing symbols to fit your app's design.

## Creating an Image

You can easily create an `Image` instance from an SFSymbol using the `.image` property. This allows you to display SF Symbols in your SwiftUI views:

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

## Customizing Colors

SFSymbol symbols are customizable. You can set the foreground color using the `.foregroundColor` modifier:

```swift
import SwiftUI
import SFSymbol

struct ContentView: View {
    var body: some View {
        SFSymbol.heart_fill.image
            .resizable()
            .scaledToFit()
            .foregroundColor(.red) // Set the symbol's color
            .frame(width: 50, height: 50)
    }
}
```

## Dot Notation

Access symbols using dot notation for improved readability and discoverability:

```swift
import SwiftUI
import SFSymbol

struct ContentView: View {
    var body: some View {
        SFSymbol.leaf.image // Access a symbol with dot notation
            .resizable()
            .scaledToFit()
            .foregroundColor(.green)
            .frame(width: 50, height: 50)
    }
}
```

## Advanced Customization

For advanced customization options and more examples, please refer to the full documentation in the [Documentation](Documentation/Usage.md) section.

Have a specific use case or need further assistance? Don't hesitate to reach out on the [SFSymbol GitHub repository](https://github.com/LuckeyLogic/SFSymbol). Happy coding!
