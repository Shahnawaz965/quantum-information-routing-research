import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "processed" / "table_iv_reproduced.csv"


class DelayModelTests(unittest.TestCase):
    def test_sixteen_hop_minimum_delay_exceeds_baseline_cutoff(self):
        hops = 16
        minimum_per_hop_us = 50.0
        cutoff_us = 100.0
        self.assertEqual(hops * minimum_per_hop_us, 800.0)
        self.assertGreater(hops * minimum_per_hop_us, cutoff_us)

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

    def test_sixteen_hop_survival_bounds_are_deterministic(self):
        with CSV_PATH.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        sixteen = {int(r["cutoff_us"]): float(r["survival_probability_mean"])
                   for r in rows if int(r["hops"]) == 16}
        self.assertEqual(sixteen[100], 0.0)
        self.assertEqual(sixteen[200], 0.0)
        self.assertEqual(sixteen[500], 0.0)
        self.assertEqual(sixteen[1000], 0.0)
        self.assertEqual(sixteen[3000], 1.0)


if __name__ == "__main__":
    unittest.main()
