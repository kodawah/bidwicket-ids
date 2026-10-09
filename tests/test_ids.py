import json
from pathlib import Path
import unittest

from bidwicket_ids import checksum, encode, shift

FIXTURES = Path(__file__).parent / "fixtures"


class EncoderTests(unittest.TestCase):
    def test_store_exports(self):
        rows = json.loads((FIXTURES / "store-637.json").read_text())
        self.assertEqual(len(rows), 52)
        for row in rows:
            with self.subTest(row=row):
                self.assertEqual(encode(row["store"], row["item"], row["variant"]), row["encoded"])

    def test_public_demo_pairs(self):
        rows = json.loads((FIXTURES / "demo-6560.json").read_text())
        self.assertEqual(len(rows), 100)
        for row in rows:
            store, plugin, item, variant, raw_check = row["raw"].split("-")
            with self.subTest(raw=row["raw"]):
                self.assertEqual(plugin, "C")
                self.assertEqual(checksum(f"{store}-C-{item}-{variant}", 883), raw_check)
                self.assertEqual(encode(store, item, variant), row["encoded"])

    def test_recorded_live_imports(self):
        rows = json.loads((FIXTURES / "live-imports.json").read_text())
        self.assertEqual(len(rows), 6)
        for row in rows:
            with self.subTest(row=row):
                self.assertEqual(encode(row["store"], row["item"], row["variant"]), row["id"])
                self.assertEqual(row["quantity"], row["exported_quantity"])

    def test_unsupported_inputs(self):
        cases = [(999, "27223", "106"), (6560, "309767", "105"),
                 (637, "1234", "106"), (637, "27223", "10"),
                 (637, "abcde", "106"), (637, "１２３４５", "106")]
        for args in cases:
            with self.subTest(args=args), self.assertRaises(ValueError):
                encode(*args)

    def test_leading_zeros_preserved(self):
        result = encode("637", "00001", "006")
        self.assertEqual(result.split("-")[3:5], ["89720", "185"])

    def test_shift_width_is_checked(self):
        with self.assertRaises(ValueError):
            shift("123", (1, 2), "0123456789")


if __name__ == "__main__":
    unittest.main()
