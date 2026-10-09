"""Reconstructed BidWicket USCIDU product-code encoder.

Only explicitly measured store profiles and identifier widths are supported.
See docs/algorithm.md for the reconstruction and validation scope.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass

CHECKSUM_ALPHABET = "ABCDEFGHIJKLMNZPQRSTUVWXY"
DIGITS = "0123456789"
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


@dataclass(frozen=True)
class Profile:
    plugin: str
    digit_offsets: tuple[int, ...]
    letter_offsets: dict[int, tuple[int, ...]]


PROFILES = {
    "637": Profile("F", (8, 9, 7, 2, 9, 1, 8, 9, 7), {
        5: (15, 4, 17), 6: (4, 17, 3),
    }),
    "6560": Profile("U", (8, 2, 1, 2, 2, 0, 8, 2), {
        5: (3, 20, 20),
    }),
}


def java_hash(text: str) -> int:
    """Return the unsigned 32-bit Java-style hash of an ASCII code."""
    value = 0
    for char in text:
        value = (31 * value + ord(char)) & 0xffffffff
    return value


def checksum(text: str, offset: int) -> str:
    value = (java_hash(text + "-") + offset) & 0xffffffff
    signed = value if value < 2**31 else value - 2**32
    magnitude = abs(signed)
    return "".join(CHECKSUM_ALPHABET[(magnitude // 26**i) % 25]
                   for i in range(3))


def shift(text: str, offsets: tuple[int, ...], alphabet: str) -> str:
    if len(text) != len(offsets):
        raise ValueError("Text and shift sequence must have equal widths")
    return "".join(alphabet[(alphabet.index(char) + offset) % len(alphabet)]
                   for char, offset in zip(text, offsets))


def encode(store_id: str | int, item_id: str | int,
           variant_id: str | int) -> str:
    """Encode a C product code using a measured store profile.

    Pass strings to preserve leading zeros. Unsupported profiles or widths
    raise ValueError rather than generating an unverified identifier.
    """
    store, item, variant = str(store_id), str(item_id), str(variant_id)
    profile = PROFILES.get(store)
    if profile is None:
        raise ValueError(f"No measured profile for store {store!r}")
    if (len(item) not in profile.letter_offsets or len(variant) != 3
            or any(char not in DIGITS for char in item + variant)):
        widths = ", ".join(str(width) for width in profile.letter_offsets)
        raise ValueError(f"Store {store} requires item width {widths} and variant width 3, using ASCII digits")
    plain_check = checksum(f"C-{item}-{variant}", 111)
    item_encoded = shift(item, profile.digit_offsets[:len(item)], DIGITS)
    variant_encoded = shift(variant, profile.digit_offsets[len(item):len(item) + 3], DIGITS)
    check_encoded = shift(plain_check, profile.letter_offsets[len(item)], LETTERS)
    prefix = f"USCIDU-{store}-{profile.plugin}-{item_encoded}-{variant_encoded}-{check_encoded}"
    return prefix + "-" + checksum(prefix, 89)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("store", help="Measured store ID: 637 or 6560")
    parser.add_argument("item", help="Original C product ID, retaining leading zeros")
    parser.add_argument("variant", help="Original three-digit variant ID")
    args = parser.parse_args()
    try:
        result = encode(args.store, args.item, args.variant)
    except ValueError as error:
        parser.error(str(error))
    print(result)


if __name__ == "__main__":
    main()
