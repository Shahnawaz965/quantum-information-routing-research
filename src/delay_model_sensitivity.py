#!/usr/bin/env python3
"""Reproduce the delay-model survival analysis (Table IV / Fig. 6).

This is a Monte Carlo delay model, not a SeQUeNCe discrete-event simulation.
Each per-hop delay is sampled independently from Uniform(50, 150) microseconds.
"""
from pathlib import Path
import csv
import math
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT_CSV = ROOT / "data" / "processed" / "table_iv_reproduced.csv"
OUT_FIG = ROOT / "figures" / "delay_model_survival.png"

HOP_COUNTS = [1, 2, 4, 8, 16]
CUTOFFS_US = [100, 200, 500, 1000, 2000, 3000]
SEEDS = 30
TRIALS_PER_SEED = 20_000
DELAY_MIN_US = 50.0
DELAY_MAX_US = 150.0


def wilson_interval(successes: int, n: int, z: float = 1.96):
    """95% Wilson score interval for a binomial proportion."""
    if n <= 0:
        return float("nan"), float("nan")
    p = successes / n
    den = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return max(0.0, centre - half), min(1.0, centre + half)


def main():
    rows = []
    for hops in HOP_COUNTS:
        age_batches = []
        for seed in range(SEEDS):
            rng = np.random.default_rng(seed + 10_000 * hops)
            delays = rng.uniform(
                DELAY_MIN_US, DELAY_MAX_US,
                size=(TRIALS_PER_SEED, hops)
            )
            age_batches.append(delays.sum(axis=1))
        ages = np.concatenate(age_batches)
        n = ages.size

        for cutoff in CUTOFFS_US:
            survived = int(np.count_nonzero(ages <= cutoff))
            low, high = wilson_interval(survived, n)
            rows.append({
                "hops": hops,
                "cutoff_us": cutoff,
                "trials": n,
                "survivals": survived,
                "survival_probability": survived / n,
                "ci95_low": low,
                "ci95_high": high,
                "delay_model": "independent Uniform(50,150) us per hop",
            })

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    OUT_FIG.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(7.0, 4.2))
    for hops in HOP_COUNTS:
        subset = [row for row in rows if row["hops"] == hops]
        plt.plot(
            [row["cutoff_us"] for row in subset],
            [row["survival_probability"] for row in subset],
            marker="o", label=f"{hops} hops"
        )
    plt.xlabel("Memory cutoff (μs)")
    plt.ylabel("P(accumulated age ≤ cutoff)")
    plt.title("Resource survival versus memory cutoff")
    plt.ylim(-0.02, 1.05)
    plt.grid(True, alpha=0.25)
    plt.legend(ncol=2, fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT_FIG, dpi=220)
    plt.close()

    print(f"CSV saved to: {OUT_CSV}")
    print(f"Figure saved to: {OUT_FIG}")
    print(f"Samples per hop count: {SEEDS * TRIALS_PER_SEED:,}")
    print("Scope: delay-model analysis only; not a SeQUeNCe simulation.")


if __name__ == "__main__":
    main()
