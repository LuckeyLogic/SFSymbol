# SFSymbol Installation Guide

This guide provides step-by-step instructions on how to add the SFSymbol Swift package to your Xcode project. SFSymbol simplifies access to Apple's SF Symbols library, offering type-safe and dot-notation access to a wide range of icons for iOS, macOS, watchOS, and tvOS development.

## Prerequisites

Before you begin, make sure you have the following prerequisites:

- Xcode installed on your development machine.

## Steps to Install SFSymbol

Follow these steps to add SFSymbol as a dependency in your Xcode project:

1. **Open Your Xcode Project**:
   - Launch Xcode and open your project.

2. **Navigate to the Project Settings**:
   - In the Xcode project navigator, select your project to open its settings.

3. **Select Your Target**:
   - In the project settings, select the target where you want to use SFSymbol.

4. **Open the Swift Package Dependencies Tab**:
   - Go to the "Swift Packages" tab.

5. **Add SFSymbol Dependency**:
   - Click the "+" button to add a package dependency.

6. **Enter the Package URL**:
   - In the "Choose Package Repository" dialog, enter the following URL:
     ```
     https://github.com/LuckeyLogic/SFSymbol.git
     ```

7. **Specify the Version**:
   - Choose the version of SFSymbol that you want to use. You can select a specific version or leave it as "Up to Next Major."

8. **Add the Dependency**:
   - Click the "Add Package" button.

9. **Confirmation**:
   - Xcode will fetch the SFSymbol package and add it to your project. You'll see it listed under "Swift Package Dependencies."

10. **Import SFSymbol**:
    - In your Swift files where you want to use SFSymbol, import the SFSymbol module at the top of your file:
      ```swift
      import SFSymbol
      ```

11. **Usage**:
    - You can now access SF Symbols using dot notation, such as:
      ```swift
      let starImage = SFSymbol.star_fill.image
      ```

12. **Build and Run**:
    - Build and run your project, and you can start using SF Symbols with SFSymbol.

## Updating SFSymbol

To update SFSymbol to a newer version in the future, follow these steps:

1. **Open Your Xcode Project**.
2. **Navigate to the Swift Package Dependencies Tab**.
3. **Select the SFSymbol Dependency**.
4. **Click the "Update to Latest Package Versions" button**.

## Conclusion

You've successfully installed SFSymbol into your Xcode project. You can now use SF Symbols in your iOS, macOS, watchOS, or tvOS application with ease.

For more advanced usage and customization options, please refer to the [Documentation](Documentation/Usage.md).

If you encounter any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request on the [SFSymbol GitHub repository](https://github.com/LuckeyLogic/SFSymbol).

Happy coding!
