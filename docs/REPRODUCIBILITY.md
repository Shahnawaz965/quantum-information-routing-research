# Reproducibility

Use Python 3.10 or newer from the repository root.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/delay_model_sensitivity.py
python src/baseline_diagnostic_simpy.py --seed 2026 --horizon-s 10
python src/audit_paper_results.py
python -m unittest discover -s tests -v
```

## Delay-model run

The model samples independent `Uniform(50,150) μs` hop delays for hop counts 1–16 and cutoffs 100, 200, 500, 1,000, 2,000, and 3,000 μs. It uses 30 seed-specific batches of 20,000 samples per hop count. The 95% confidence interval is calculated using a Student-t interval across the 30 seed-level proportions.

Outputs are saved under `data/processed/` and `figures/`.

## Baseline reconstruction

The second script reconstructs the supplied generation-and-forwarding event loop using SimPy. It uses seed 2026 by default and can write new values that differ from the paper's one-run snapshot. It is explicitly **not SeQUeNCe**, and its output must not be used to validate the paper's SeQUeNCe claim.

## Provenance

- Paper-stated baseline values are in `data/raw/supplied_baseline_configuration.csv`.
- Table IV values transcribed from a supplied output are in `data/raw/table_iv_values_as_supplied.csv`.
- Candidate Tables V and VI are retained in `data/raw/supplied_table_V_VI_candidate_values.csv`, marked unverified.
- The original SeQUeNCe source, topology/configuration, RNG seeds, and event logs have not been supplied; Table V/VI performance claims therefore remain unverified.
