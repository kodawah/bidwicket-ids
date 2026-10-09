# bidwicket-ids

A small, dependency-free Python encoder for BidWicket `USCIDU` product IDs,
reconstructed from public examples and verified against exported codes.

It generates the full identifier, including both three-letter groups, from
an original `C` product code. This allows CSV import files to be built locally
for the supported store profiles.

## Usage

Requires Python 3.9 or newer. No installation or network access is needed.

```sh
python3 bidwicket_ids.py 6560 49055 106
# USCIDU-6560-U-21177-188-VBE-ABW

python3 bidwicket_ids.py 637 27223 106
# USCIDU-637-F-06942-285-SIN-ZGM
```

```python
from bidwicket_ids import encode

identifier = encode(store_id="637", item_id="309767", variant_id="105")
# USCIDU-637-F-196958-992-RTJ-AVC
```

Supply the **original C product and variant numbers**, retaining leading zeros.
Do not supply the already encoded numbers from a storefront's product URL.

## Supported profiles

| Store ID | Input plugin | Encoded plugin | Product width | Variant width |
| --- | --- | --- | --- | --- |
| 637 | C | F | 5 or 6 digits | 3 digits |
| 6560 | C | U | 5 digits | 3 digits |

These are measured profiles, not a general key derivation for every store.
Unsupported stores and widths are rejected.

## Verification

```sh
python3 -m unittest discover -s tests -v
```

The fixtures cover 52 distinct export IDs for profile 637 and 100 public
BidWicket demo pairs for profile 6560. Six profile-637 IDs were generated
before export and accepted in two live, three-row CSV imports; the subsequent
exports matched the predictions and quantities. Tests replay the recorded
results locally and do not contact a storefront.

See [the reconstruction](docs/algorithm.md) and [CSV import notes](docs/csv-import.md).
This is an independent research implementation, not an official BidWicket SDK.
