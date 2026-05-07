#!/usr/bin/env python3
"""
SF Symbols code generator.

Reads Apple's SF Symbols catalog from
  /Applications/SF Symbols.app/Contents/Resources/Metadata/name_availability.plist

and emits two Swift sources:

  1. Sources/SFSymbol/SFSymbol.swift
        Legacy `enum SFSymbol: String` with one underscored case per symbol.

  2. Sources/SFSymbolKit/Generated/*.swift
        Strict, type-safe nested namespaces. Each symbol path becomes a chain
        of caseless enums; leaves expose `image` and `name`.

Run from repo root:
    python3 Tools/generate.py

Use --check to verify generated files match the catalog without writing.
"""

from __future__ import annotations

import argparse
import json
import os
import plistlib
import re
import string
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DEFAULT_CATALOG = Path(
    "/Applications/SF Symbols.app/Contents/Resources/Metadata/name_availability.plist"
)
REPO_ROOT = Path(__file__).resolve().parent.parent
LEGACY_OUT = REPO_ROOT / "Sources" / "SFSymbol" / "SFSymbol.swift"
KIT_OUT_DIR = REPO_ROOT / "Sources" / "SFSymbolKit" / "Generated"
KIT_ROOT_FILE = REPO_ROOT / "Sources" / "SFSymbolKit" / "SFSymbol.swift"

# Apple substitutes these locale variants automatically based on the user's
# locale, so we do NOT expose them as separate Swift identifiers.
LOCALE_SUFFIXES = {
    "ar", "he", "hi", "bn", "gu", "ka", "km", "kn", "lo", "ml", "mm", "mni",
    "mr", "my", "ne", "or", "pa", "sa", "sat", "si", "ta", "te", "th", "rtl",
    "ja", "ko", "zh", "el", "ru",
}

# Swift reserved words that may appear as segments inside a symbol path.
SWIFT_KEYWORDS = {
    "case", "return", "repeat", "class", "struct", "enum", "func", "let",
    "var", "if", "else", "for", "while", "do", "switch", "default", "break",
    "continue", "guard", "defer", "throw", "throws", "rethrows", "try",
    "catch", "as", "is", "in", "where", "self", "Self", "super", "init",
    "deinit", "extension", "protocol", "typealias", "associatedtype",
    "operator", "infix", "prefix", "postfix", "inout", "mutating",
    "nonmutating", "public", "private", "fileprivate", "internal", "open",
    "final", "static", "dynamic", "lazy", "weak", "unowned", "optional",
    "required", "convenience", "indirect", "some", "any", "await", "async",
    "true", "false", "nil", "subscript",
}

# Names used as leaf accessors on every node. A path segment matching one of
# these would collide with the static accessor in Swift, so colliding child
# segments get a trailing underscore in the dot-notation API.
KIT_LEAF_ACCESSORS = {"image", "name"}

# Map Apple's catalog year (and optional minor) to the minimum Apple OS
# version that ships the symbol. Apple releases SF Symbols updates with
# specific OS point releases; we floor to year-major because Apple does not
# publish an authoritative minor-version mapping.
#
# Note: macOS support for `Image(systemName:)` starts at macOS 11.0
# (SwiftUI lifted the system-image baseline in Big Sur), so even SF Symbols 1
# is gated to macOS 11 from our point of view.
YEAR_TO_OS = {
    "2019": ("13.0", "11.0", "6.0", "13.0"),
    "2020": ("14.0", "11.0", "7.0", "14.0"),
    "2021": ("15.0", "12.0", "8.0", "15.0"),
    "2022": ("16.0", "13.0", "9.0", "16.0"),
    "2023": ("17.0", "14.0", "10.0", "17.0"),
    "2024": ("18.0", "15.0", "11.0", "18.0"),
    "2025": ("19.0", "16.0", "12.0", "19.0"),
}


# ---------------------------------------------------------------------------
# Catalog parsing
# ---------------------------------------------------------------------------


def load_catalog(path: Path) -> dict[str, str]:
    """Return mapping of symbol-name -> first-available year string."""
    with path.open("rb") as f:
        data = plistlib.load(f)
    return data["symbols"]


def is_locale_variant(name: str) -> bool:
    parts = name.split(".")
    if not parts:
        return False
    if parts[-1] in ("fixed", "traditional"):
        return len(parts) >= 2 and parts[-2] in LOCALE_SUFFIXES
    return parts[-1] in LOCALE_SUFFIXES


def filter_catalog(catalog: dict[str, str]) -> dict[str, str]:
    return {n: v for n, v in catalog.items() if not is_locale_variant(n)}


# ---------------------------------------------------------------------------
# Identifier mangling
# ---------------------------------------------------------------------------


def legacy_identifier(symbol_name: str) -> str:
    """Convert "square.and.arrow.up" -> "square_and_arrow_up".

    Leading-digit names get a leading underscore (e.g. "4k.tv" -> "_4k_tv").
    Keyword names get a leading underscore (e.g. "repeat" -> "_repeat").
    """
    ident = symbol_name.replace(".", "_")
    if ident[0].isdigit():
        ident = "_" + ident
    elif ident in SWIFT_KEYWORDS:
        ident = "_" + ident
    return ident


def kit_segment_identifier(segment: str, parent_is_leaf: bool = False) -> str:
    """Convert a single path segment into a Swift identifier.

    Leading-digit segments get a leading underscore; keyword segments are
    backticked. Segments that would collide with a leaf accessor on a leaf
    parent get a trailing underscore.
    """
    if parent_is_leaf and segment in KIT_LEAF_ACCESSORS:
        return segment + "_"
    if segment and segment[0].isdigit():
        return "_" + segment
    if segment in SWIFT_KEYWORDS:
        return f"`{segment}`"
    return segment


# ---------------------------------------------------------------------------
# Availability
# ---------------------------------------------------------------------------


def availability_clause(year: str) -> str:
    """Return @available(...) for a given Apple year string ("2024", "2024.3")."""
    major = year.split(".")[0]
    iOS, macOS, watchOS, tvOS = YEAR_TO_OS[major]
    return (
        f"@available(iOS {iOS}, macOS {macOS}, watchOS {watchOS}, tvOS {tvOS}, *)"
    )


# ---------------------------------------------------------------------------
# Trie for SFSymbolKit
# ---------------------------------------------------------------------------


@dataclass
class TrieNode:
    name: str = ""               # raw segment name, e.g. "fill"
    is_leaf: bool = False        # this path is itself a symbol
    leaf_year: Optional[str] = None  # availability year if leaf
    full_name: str = ""          # full dotted path, e.g. "star.circle.fill"
    children: dict[str, "TrieNode"] = field(default_factory=dict)


def build_trie(symbols: dict[str, str]) -> TrieNode:
    root = TrieNode(name="<root>")
    for path, year in symbols.items():
        parts = path.split(".")
        node = root
        for i, part in enumerate(parts):
            if part not in node.children:
                node.children[part] = TrieNode(name=part)
            node = node.children[part]
            if i == len(parts) - 1:
                node.is_leaf = True
                node.leaf_year = year
                node.full_name = path
    return root


def min_subtree_year(node: TrieNode) -> Optional[str]:
    """Return the lowest Apple-year string in this node's subtree.

    Used to pick a single @available for an intermediate enum that doesn't
    correspond to a real symbol but contains real symbols beneath it.
    """
    candidates: list[str] = []
    if node.is_leaf and node.leaf_year:
        candidates.append(node.leaf_year)
    for child in node.children.values():
        sub = min_subtree_year(child)
        if sub:
            candidates.append(sub)
    if not candidates:
        return None

    def key(y: str):
        major, *rest = y.split(".")
        return (int(major), int(rest[0]) if rest else 0)

    return min(candidates, key=key)


# ---------------------------------------------------------------------------
# Legacy enum emitter
# ---------------------------------------------------------------------------


LEGACY_HEADER = '''// AUTO-GENERATED by Tools/generate.py from Apple's SF Symbols catalog.
// Do not edit by hand. Run `python3 Tools/generate.py` to regenerate.
//
//  SFSymbol.swift
//
//  Created by Miguel Brown on 5/9/22.
//  Copyright © 2022-{year} Luckey Logic. All rights reserved.
//
//  SF Symbols catalog version: {sf_version}
//  Generated {symbol_count} symbols from {raw_count} catalog entries
//  ({locale_filtered} locale variants filtered).
//
//  Naming conventions:
//    - Dots in symbol names become underscores ("star.fill" -> "star_fill").
//    - Symbols starting with a digit get a leading underscore ("4k.tv" -> "_4k_tv").
//    - Symbols matching Swift keywords get a leading underscore ("repeat" -> "_repeat").
//
//  Usage:
//      let starImage = SFSymbol.star_fill.image
//
//  This API style is preserved for backwards compatibility.
//  See SFSymbolKit for the type-safe dot-notation API.

import SwiftUI

@available(iOS 13.0, macOS 11.0, watchOS 6.0, tvOS 13.0, *)
public enum SFSymbol: String, CustomStringConvertible {{

    /// Returns an `Image` instance for the corresponding SF Symbol.
    public var image: Image {{ Image(systemName: self.rawValue) }}

    /// The raw SF Symbols name (e.g. `"star.fill"`).
    public var description: String {{ self.rawValue }}

    // MARK: - Symbols
'''

LEGACY_FOOTER = '''
}
'''


def emit_legacy(symbols: dict[str, str], sf_version: str, raw_count: int) -> str:
    out: list[str] = []
    out.append(LEGACY_HEADER.format(
        year="2026",
        sf_version=sf_version,
        symbol_count=len(symbols),
        raw_count=raw_count,
        locale_filtered=raw_count - len(symbols),
    ))

    seen_idents: dict[str, str] = {}
    sorted_names = sorted(symbols.keys())
    for name in sorted_names:
        ident = legacy_identifier(name)
        if ident in seen_idents:
            # Two distinct symbol names mangling to the same identifier.
            # Skip the second; record so a human can resolve.
            print(
                f"warning: identifier collision: {name!r} and "
                f"{seen_idents[ident]!r} both -> {ident!r}; skipping {name!r}",
                file=sys.stderr,
            )
            continue
        seen_idents[ident] = name
        # Pad identifier to a fixed column for readability, matching the
        # historical formatting in the legacy file.
        out.append(f'    case {ident:<100} = "{name}"')

    out.append(LEGACY_FOOTER)
    return "\n".join(out)


# ---------------------------------------------------------------------------
# SFSymbolKit emitter
# ---------------------------------------------------------------------------


KIT_ROOT = '''// AUTO-GENERATED root for SFSymbolKit.
// Do not edit by hand. Run `python3 Tools/generate.py` to regenerate.
//
//  SFSymbol.swift
//  SFSymbolKit
//
//  Type-safe dot-notation access to Apple's SF Symbols.
//
//  Usage:
//      import SFSymbolKit
//      let starImage = SFSymbol.star.fill.image
//
//  Each symbol leaf exposes `image` (a SwiftUI `Image`) and `name`
//  (the raw SF Symbols string).
//
//  Reserved Swift keywords appear as backticked identifiers, e.g.
//  `SFSymbol.\\`case\\`.image`. Names starting with a digit are prefixed
//  with `_`, e.g. `SFSymbol._4k.tv.image` for `4k.tv`.

import SwiftUI

@available(iOS 13.0, macOS 11.0, watchOS 6.0, tvOS 13.0, *)
public enum SFSymbol {}
'''


KIT_FILE_HEADER = '''// AUTO-GENERATED — do not edit. Generated by Tools/generate.py
// SF Symbols catalog version: {sf_version}
// File: symbols beginning with `{bucket}`

import SwiftUI

'''


def emit_kit_node(
    node: TrieNode,
    parent_path: list[str],
    indent: int,
    out: list[str],
    in_public_extension: bool = False,
    parent_is_leaf: bool = False,
) -> None:
    """Emit a nested enum for a single trie node.

    `parent_path` is the chain of mangled identifiers from SFSymbol downward.
    `indent` is the current leading-space count.
    `in_public_extension` is True when this node is a direct child of a
    `public extension` block (where `public` on members is redundant).
    `parent_is_leaf` is True when the parent node defines `image`/`name`
    accessors that would collide with a child of the same segment name.
    """
    pad = " " * indent
    swift_seg = kit_segment_identifier(node.name, parent_is_leaf=parent_is_leaf)
    avail_year = min_subtree_year(node)
    avail = availability_clause(avail_year) if avail_year else ""
    access = "" if in_public_extension else "public "

    if avail:
        out.append(f"{pad}{avail}")
    out.append(f"{pad}{access}enum {swift_seg} {{")

    if node.is_leaf and node.leaf_year:
        leaf_avail = availability_clause(node.leaf_year)
        # Static accessors for the symbol itself.
        out.append(f"{pad}    {leaf_avail}")
        out.append(
            f'{pad}    public static var image: Image '
            f'{{ Image(systemName: "{node.full_name}") }}'
        )
        out.append(f"{pad}    {leaf_avail}")
        out.append(
            f'{pad}    public static var name: String {{ "{node.full_name}" }}'
        )

    for child_name in sorted(node.children.keys()):
        emit_kit_node(
            node.children[child_name],
            parent_path + [swift_seg],
            indent + 4,
            out,
            in_public_extension=False,
            parent_is_leaf=node.is_leaf,
        )

    out.append(f"{pad}}}")


def bucket_for_segment(segment: str) -> str:
    """Pick a filename bucket for a top-level segment.

    All digit-starting top-levels share `_digits`. Letters bucket by lowercase
    first character. Keeps generated files balanced.
    """
    if segment[0].isdigit():
        return "_digits"
    return segment[0].lower()


def emit_kit(trie: TrieNode, sf_version: str) -> dict[Path, str]:
    """Produce a mapping of file path -> file contents for SFSymbolKit."""
    files: dict[Path, str] = {}

    # Group top-level children by bucket so each output file extends
    # SFSymbol with a subset of nested enums.
    buckets: dict[str, list[TrieNode]] = defaultdict(list)
    for child_name in sorted(trie.children.keys()):
        child = trie.children[child_name]
        buckets[bucket_for_segment(child_name)].append(child)

    for bucket, children in sorted(buckets.items()):
        body: list[str] = []
        body.append(KIT_FILE_HEADER.format(sf_version=sf_version, bucket=bucket))
        body.append("@available(iOS 13.0, macOS 11.0, watchOS 6.0, tvOS 13.0, *)")
        body.append("public extension SFSymbol {")
        for child in children:
            emit_kit_node(
                child, ["SFSymbol"], indent=4, out=body,
                in_public_extension=True,
            )
        body.append("}")
        body.append("")
        files[KIT_OUT_DIR / f"SFSymbol+{bucket}.swift"] = "\n".join(body)

    return files


# ---------------------------------------------------------------------------
# SF Symbols version detection
# ---------------------------------------------------------------------------


def detect_sf_version() -> str:
    """Read SF Symbols.app's CFBundleShortVersionString."""
    plist = Path("/Applications/SF Symbols.app/Contents/Info.plist")
    if not plist.exists():
        return "unknown"
    try:
        with plist.open("rb") as f:
            info = plistlib.load(f)
        version = info.get("CFBundleShortVersionString", "?")
        build = info.get("CFBundleVersion", "?")
        return f"{version} ({build})"
    except Exception:
        return "unknown"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--catalog", type=Path, default=DEFAULT_CATALOG,
        help="Path to name_availability.plist",
    )
    parser.add_argument(
        "--legacy-only", action="store_true",
        help="Only regenerate the legacy SFSymbol enum",
    )
    parser.add_argument(
        "--kit-only", action="store_true",
        help="Only regenerate SFSymbolKit",
    )
    parser.add_argument(
        "--check", action="store_true",
        help="Verify outputs are up to date without writing",
    )
    args = parser.parse_args(argv)

    if not args.catalog.exists():
        print(f"error: catalog not found at {args.catalog}", file=sys.stderr)
        print(
            "Install SF Symbols.app from https://developer.apple.com/sf-symbols/",
            file=sys.stderr,
        )
        return 1

    raw = load_catalog(args.catalog)
    filtered = filter_catalog(raw)
    sf_version = detect_sf_version()

    print(f"SF Symbols version: {sf_version}", file=sys.stderr)
    print(f"Catalog entries:    {len(raw)}", file=sys.stderr)
    print(f"After locale filter: {len(filtered)}", file=sys.stderr)

    write_legacy = not args.kit_only
    write_kit = not args.legacy_only

    if write_legacy:
        legacy_src = emit_legacy(filtered, sf_version, len(raw))
        if args.check:
            existing = LEGACY_OUT.read_text() if LEGACY_OUT.exists() else ""
            if existing.strip() != legacy_src.strip():
                print("legacy SFSymbol.swift is out of date", file=sys.stderr)
                return 2
        else:
            LEGACY_OUT.parent.mkdir(parents=True, exist_ok=True)
            LEGACY_OUT.write_text(legacy_src)
            print(f"wrote {LEGACY_OUT.relative_to(REPO_ROOT)}", file=sys.stderr)

    if write_kit:
        kit_files = emit_kit(build_trie(filtered), sf_version)
        if args.check:
            for path, content in kit_files.items():
                existing = path.read_text() if path.exists() else ""
                if existing.strip() != content.strip():
                    print(f"{path.relative_to(REPO_ROOT)} is out of date", file=sys.stderr)
                    return 2
        else:
            KIT_OUT_DIR.mkdir(parents=True, exist_ok=True)
            # Wipe stale generated files in the directory.
            for stale in KIT_OUT_DIR.glob("SFSymbol+*.swift"):
                stale.unlink()
            for path, content in kit_files.items():
                path.write_text(content)
            KIT_ROOT_FILE.parent.mkdir(parents=True, exist_ok=True)
            KIT_ROOT_FILE.write_text(KIT_ROOT)
            print(
                f"wrote {len(kit_files)} files under "
                f"{KIT_OUT_DIR.relative_to(REPO_ROOT)}/",
                file=sys.stderr,
            )

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
