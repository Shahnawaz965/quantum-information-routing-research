#!/usr/bin/env python3
"""Reproduce delay-model survival sensitivity for Table IV / Fig. 6.

This is a Monte Carlo delay model, not a SeQUeNCe discrete-event simulation.
For each hop count H, each per-hop delay is independent Uniform(50, 150) us.
Each seed contributes 20,000 trials; estimates and Student-t 95% confidence
intervals are calculated across the 30 seed-level survival proportions.
"""
from pathlib import Path
import csv
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT_CSV = ROOT / "data" / "processed" / "table_iv_reproduced.csv"
OUT_FIG = ROOT / "figures" / "delay_model_survival.png"

HOP_COUNTS = list(range(1, 17))
CUTOFFS_US = [100, 200, 500, 1000, 2000, 3000]
SEEDS = 30
TRIALS_PER_SEED = 20_000
DELAY_MIN_US = 50.0
DELAY_MAX_US = 150.0
T_CRITICAL_DF29 = 2.045229642  # two-sided 95% Student-t critical value, df=29


def mean_ci95(values):
    """Return sample mean and 95% Student-t CI half-width across seeds."""
    values = np.asarray(values, dtype=float)
    mean = float(np.mean(values))
    if len(values) < 2:
        return mean, float("nan")
    sd = float(np.std(values, ddof=1))
    half_width = T_CRITICAL_DF29 * sd / np.sqrt(len(values))
    return mean, half_width


def main():
    rows = []
    # Deterministic seed schedule makes a repeated run reproducible.
    for hops in HOP_COUNTS:
        seed_ages = []
        for seed in range(SEEDS):
            rng = np.random.default_rng(seed + 10_000 * hops)
            delays = rng.uniform(
                DELAY_MIN_US, DELAY_MAX_US,
                size=(TRIALS_PER_SEED, hops)
            )
            seed_ages.append(delays.sum(axis=1))

        for cutoff in CUTOFFS_US:
            seed_probabilities = [
                float(np.mean(ages <= cutoff)) for ages in seed_ages
            ]
            mean, ci_half_width = mean_ci95(seed_probabilities)
            rows.append({
                "hops": hops,
                "cutoff_us": cutoff,
                "seeds": SEEDS,
                "trials_per_seed": TRIALS_PER_SEED,
                "total_trials": SEEDS * TRIALS_PER_SEED,
                "survival_probability_mean": mean,
                "ci95_half_width_across_seeds": ci_half_width,
                "ci95_low": max(0.0, mean - ci_half_width),
                "ci95_high": min(1.0, mean + ci_half_width),
                "delay_model": "independent Uniform(50,150) us per hop",
            })

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    OUT_FIG.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(9.0, 5.4))
    for hops in HOP_COUNTS:
        subset = [row for row in rows if row["hops"] == hops]
        plt.plot(
            [row["cutoff_us"] for row in subset],
            [row["survival_probability_mean"] for row in subset],
            marker="o", markersize=2.5, linewidth=1,
            label=f"{hops} hop" if hops == 1 else f"{hops} hops"
        )
    plt.xlabel("Memory cutoff (μs)")
    plt.ylabel("P(accumulated age ≤ cutoff)")
    plt.title("Resource survival versus memory cutoff")
    plt.ylim(-0.02, 1.05)
    plt.grid(True, alpha=0.25)
    plt.legend(ncol=4, fontsize=7)
    plt.tight_layout()
    plt.savefig(OUT_FIG, dpi=220)
    plt.close()

    print(f"CSV saved to: {OUT_CSV}")
    print(f"Figure saved to: {OUT_FIG}")
    print(f"Seeds: {SEEDS}; trials/seed/hop-count: {TRIALS_PER_SEED:,}")
    print("Scope: delay-model analysis only; not a SeQUeNCe simulation.")


if __name__ == "__main__":
    main()
