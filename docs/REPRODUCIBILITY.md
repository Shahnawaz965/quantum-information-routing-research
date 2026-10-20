# Reproducibility

From the repository root, use Python 3.10 or newer:

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    python src/delay_model_sensitivity.py
    python src/audit_paper_results.py

The delay-model script estimates survival for hop counts 1–16 and cutoffs 100, 200, 500, 1000, 2000, and 3000 μs. For each hop count it runs 30 seed-specific batches of 20,000 samples. Reported confidence intervals are Student-t intervals across seed-level survival proportions.

This is not a SeQUeNCe simulation. The raw SeQUeNCe source/configuration/seeds/events were not supplied. Candidate Table V/VI numbers are kept in the raw data with clear provenance labels and must not be treated as verified before comparison with source logs.
