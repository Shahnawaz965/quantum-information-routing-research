import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "processed" / "table_iv_reproduced.csv"


class DelayModelTests(unittest.TestCase):
    def test_sixteen_hop_minimum_delay_exceeds_baseline_cutoff(self):
        # Under the stated delay support, every one of the 16 delays is >=50 us.
        min_total_us = 16 * 50.0
        self.assertEqual(min_total_us, 800.0)
        self.assertGreater(min_total_us, 100.0)

    def test_output_csv_has_all_hops_and_cutoffs(self):
        self.assertTrue(CSV_PATH.exists(), "Run src/delay_model_sensitivity.py first.")
        with CSV_PATH.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 16 * 6)
        self.assertEqual({int(row["hops"]) for row in rows}, set(range(1, 17)))
        self.assertEqual(
            {int(row["cutoff_us"]) for row in rows},
            {100, 200, 500, 1000, 2000, 3000},
        )

    def test_probabilities_and_confidence_intervals_are_valid(self):
        with CSV_PATH.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        for row in rows:
            p = float(row["survival_probability_mean"])
            low = float(row["ci95_low"])
            high = float(row["ci95_high"])
            self.assertGreaterEqual(p, 0.0)
            self.assertLessEqual(p, 1.0)
            self.assertGreaterEqual(low, 0.0)
            self.assertLessEqual(low, p + 1e-12)
            self.assertGreaterEqual(high, p - 1e-12)
            self.assertLessEqual(high, 1.0)

    def test_mathematically_deterministic_sixteen_hop_cutoffs(self):
        with CSV_PATH.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        sixteen = {
            int(row["cutoff_us"]): float(row["survival_probability_mean"])
            for row in rows if int(row["hops"]) == 16
        }
        # Any cutoff below the 800 us minimum must have zero survival.
        for cutoff in (100, 200, 500):
            self.assertEqual(sixteen[cutoff], 0.0)
        # 3000 us exceeds the 2400 us maximum possible age.
        self.assertEqual(sixteen[3000], 1.0)
        # 1000 and 2000 us are not deterministic bounds; do not assert them.

if __name__ == "__main__":
    unittest.main()
