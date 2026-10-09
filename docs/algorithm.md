# USCIDU reconstruction

Research date: 9 October 2026.

The public [BidWicket theme demo](http://bidwicket.com/Help/Theme.html)
contains 100 paired raw and encoded identifiers in its HTML, including:

```
6560-C-49055-106-JXY
USCIDU-6560-U-21177-188-VBE-ABW
```

These pairs exposed the relationship between checksums and store-specific
character shifts. The formulas here reproduce the measured results; they
are an empirically recovered equivalent, not recovered server source code.

## Checksum

1. Append a hyphen to the input text.
2. Compute its Java-style hash with `h = 31*h + ord(character)`, wrapping
   to 32 bits at each step. All supported identifier characters are ASCII.
3. Add the checksum offset, wrap to 32 bits, interpret as a signed integer,
   then take its mathematical absolute value.
4. Emit three characters in order, using
   `alphabet[(n // 26**i) % 25]` for `i = 0, 1, 2`.

The exact alphabet is `ABCDEFGHIJKLMNZPQRSTUVWXY`: 25 characters, with Z
where O would ordinarily appear. Division uses 26 while selection uses 25.
Letter shifts use the ordinary 26-letter alphabet instead.

## Encoding

First calculate `checksum("C-<item>-<variant>", 111)`. Shift the product and
variant digits modulo ten using the store's position offsets; concatenate
those fields for position counting but retain their original widths.
Shift the three checksum letters modulo 26. The measured profiles are:

| Store | Encoded plugin | Digit shifts | Checksum letter shifts |
| --- | --- | --- | --- |
| 637 | F | 8,9,7,2,9,1,8,9,7 | 5-digit item: 15,4,17; 6-digit: 4,17,3 |
| 6560 | U | 8,2,1,2,2,0,8,2 | 5-digit item: 3,20,20 |

Build `USCIDU-<store>-<plugin>-<encoded item>-<encoded variant>-<encoded check>`.
Append a hyphen and `checksum(that_prefix, 89)`.

For example, `C-27223-106` has plaintext checksum `DEW`; profile 637 yields
`USCIDU-637-F-06942-285-SIN-ZGM`.

The demo's separate raw checksum can also be reproduced with
`checksum("6560-C-<item>-<variant>", 883)`. It is not the plaintext body
checksum used to construct the first encoded letter group.

## Evidence and limits

- `tests/fixtures/demo-6560.json`: 100 raw/encoded pairs from the public demo.
- `tests/fixtures/store-637.json`: 52 distinct observed export IDs.
- `tests/fixtures/live-imports.json`: six predictions accepted by live CSV
  imports, with quantities transcribed from subsequent exports.

The live cases include five- and six-digit items, multiple condition variants,
and foil finishes. The live evidence is a recorded observation, not an
ongoing integration test. Raw cart pages, session cookies, store names, and
customer data are not included.

Other stores, plugins, field widths, and games require independent measurement.
The offsets above do not establish how arbitrary store profiles are derived.
