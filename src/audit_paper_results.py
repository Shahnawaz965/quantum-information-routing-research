#!/usr/bin/env python3
"""Audit core numerical statements in the supplied research paper."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "processed" / "result_audit.txt"

hop_count = 16
min_hop_delay_us = 50.0
max_hop_delay_us = 150.0
cutoff_us = 100.0
generation_probability_per_trial = 1e-5 * (10 ** (-(10.0 * 0.2) / 10.0))
reported_trials = 434_440
expected_generations = reported_trials * generation_probability_per_trial
min_total = hop_count * min_hop_delay_us
max_total = hop_count * max_hop_delay_us
mean_total = hop_count * (min_hop_delay_us + max_hop_delay_us) / 2
sd_total = (hop_count * ((max_hop_delay_us - min_hop_delay_us) ** 2) / 12) ** 0.5

lines = [
    "RESULT AUDIT — Simulating Information Routing in Quantum Networks",
    "",
    "DELAY MODEL: independent Uniform(50,150) us delay per hop",
    f"Hops: {hop_count}",
    f"Minimum total delay: {min_total:.1f} us",
    f"Mean total delay: {mean_total:.1f} us",
    f"Maximum total delay: {max_total:.1f} us",
    f"Standard deviation of total: {sd_total:.1f} us",
    f"Memory cutoff: {cutoff_us:.1f} us",
    f"Conclusion: {'deterministic expiry' if min_total > cutoff_us else 'survival may be possible'}",
    "",
    "PAPER-REPORTED BASELINE (recorded here, not independently reproduced):",
    "Attempts=434440; generated=1; successful end-to-end links=0;",
    "purged=1; usable-entanglement rate=0.00%.",
    "",
    "GENERATION-YIELD CONSISTENCY:",
    f"Per-trial probability from supplied parameters: {generation_probability_per_trial:.8g}",
    f"Expected generated resources over 434440 trials: {expected_generations:.3f}",
    "An observed count of one is statistically plausible for this low-yield model.",
    "",
    "SIMULATOR PROVENANCE:",
    "A companion baseline prototype in the working materials uses SimPy, not",
    "SeQUeNCe. It must not be cited as the SeQUeNCe implementation described",
    "by the manuscript. The original SeQUeNCe source/configuration and raw",
    "event logs were not present in the supplied materials.",
    "",
    "TABLE V / VI PROVENANCE:",
    "A separate candidate table PDF was supplied, but no raw per-seed logs or",
    "source implementation were available to validate its policy metrics.",
    "No policy-performance claims or replacement values are generated here.",
    "",
    "SCOPE: this audit checks arithmetic and provenance; it does not prove the",
    "quantum-network simulator or the routing policy implementation is correct."
]
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines))
print(f"Saved: {OUT}")
