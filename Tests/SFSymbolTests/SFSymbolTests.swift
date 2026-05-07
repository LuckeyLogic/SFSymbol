import XCTest
import SwiftUI
@testable import SFSymbol
@testable import SFSymbolKit

final class LegacySFSymbolTests: XCTestCase {
    func test_rawValue_matchesAppleName() {
        XCTAssertEqual(SFSymbol.star.rawValue, "star")
        XCTAssertEqual(SFSymbol.star_fill.rawValue, "star.fill")
        XCTAssertEqual(SFSymbol.square_and_arrow_up.rawValue, "square.and.arrow.up")
    }

    func test_description_matchesRawValue() {
        XCTAssertEqual(SFSymbol.heart_fill.description, "heart.fill")
    }

    func test_leadingDigit_isUnderscored() {
        XCTAssertEqual(SFSymbol._4k_tv.rawValue, "4k.tv")
    }

    func test_swiftKeyword_isUnderscored() {
        XCTAssertEqual(SFSymbol._repeat.rawValue, "repeat")
        XCTAssertEqual(SFSymbol._return.rawValue, "return")
        XCTAssertEqual(SFSymbol._case.rawValue, "case")
    }

    func test_image_isCreated() {
        // Image cannot be inspected at the SwiftUI level, but the call
        // should compile and not throw.
        _ = SFSymbol.star.image
    }
}

final class SFSymbolKitTests: XCTestCase {
    func test_root_symbol_name() {
        XCTAssertEqual(SFSymbolKit.SFSymbol.star.name, "star")
    }

    func test_one_level_chain() {
        XCTAssertEqual(SFSymbolKit.SFSymbol.star.fill.name, "star.fill")
        XCTAssertEqual(SFSymbolKit.SFSymbol.heart.fill.name, "heart.fill")
    }

    func test_deep_chain() {
        XCTAssertEqual(
            SFSymbolKit.SFSymbol.square.and.arrow.up.name,
            "square.and.arrow.up"
        )
        XCTAssertEqual(
            SFSymbolKit.SFSymbol.square.and.arrow.up.fill.name,
            "square.and.arrow.up.fill"
        )
    }

    func test_leadingDigit_segment() {
        XCTAssertEqual(SFSymbolKit.SFSymbol._4k.tv.name, "4k.tv")
    }

    func test_keyword_segment_uses_backticks() {
        // Backticks at the call site escape the reserved word.
        XCTAssertEqual(SFSymbolKit.SFSymbol.`case`.name, "case")
        XCTAssertEqual(SFSymbolKit.SFSymbol.`repeat`.name, "repeat")
        XCTAssertEqual(SFSymbolKit.SFSymbol.`return`.name, "return")
    }

    func test_image_isCreated() {
        _ = SFSymbolKit.SFSymbol.star.fill.image
    }

    func test_digit_in_middle_segment() {
        // "person.2.fill" — middle segment starts with a digit, so it
        // becomes "._2" in the dot path.
        XCTAssertEqual(SFSymbolKit.SFSymbol.person._2.fill.name, "person.2.fill")
    }

    @available(iOS 18.0, macOS 15.0, watchOS 11.0, tvOS 18.0, *)
    func test_doc_text_image_collision_uses_trailing_underscore() {
        // "doc.text" is a leaf; "doc.text.image" is a separate leaf added
        // in SF Symbols 6 (iOS 18). The child segment is renamed with a
        // trailing underscore so the leaf accessor on the parent doesn't
        // collide.
        XCTAssertEqual(SFSymbolKit.SFSymbol.doc.text.name, "doc.text")
        XCTAssertEqual(SFSymbolKit.SFSymbol.doc.text.image_.name, "doc.text.image")
        XCTAssertEqual(SFSymbolKit.SFSymbol.doc.text.image_.fill.name, "doc.text.image.fill")
    }

    @available(iOS 18.0, macOS 15.0, watchOS 11.0, tvOS 18.0, *)
    func test_apple_image_playground() {
        // "apple.image" is NOT a leaf (no `image` accessor on it), so the
        // child "apple.image.playground" lives under the regular name.
        XCTAssertEqual(
            SFSymbolKit.SFSymbol.apple.image.playground.name,
            "apple.image.playground"
        )
    }
}
