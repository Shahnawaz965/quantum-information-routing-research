# Simulating Information Routing in Quantum Networks

Research-code companion to **“Simulating Information Routing in Quantum Networks.”**

## What is included

- `src/delay_model_sensitivity.py`: reproducible Monte Carlo delay-model analysis for 1–16 hops and memory cutoffs of 100, 200, 500, 1,000, 2,000, and 3,000 μs.
- `src/audit_paper_results.py`: arithmetic consistency check for the manuscript's 16-hop, 100 μs-cutoff conclusion.
- `data/raw/supplied_baseline_configuration.csv`: baseline numbers stated in the supplied paper.
- `data/raw/table_iv_values_as_supplied.csv`: values transcribed from the supplied completed Table IV PDF.
- `data/raw/supplied_table_V_VI_candidate_values.csv`: candidate policy/ablation values from the separately supplied table PDF; they are explicitly marked unverified.
- `docs/RESULT_AUDIT.md`: consistency findings, uncertainties, and recommendations.

## Run on macOS/Linux

Python 3.10+ recommended.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/delay_model_sensitivity.py
python src/audit_paper_results.py
```

The simulation script writes `data/processed/table_iv_reproduced.csv` and `figures/delay_model_survival.png`.

## Model definition

For a path with H hops, each hop delay is independent and uniformly distributed:

`D_i ~ Uniform(50, 150) μs`

The accumulated age is `A_H = sum(D_i)`. The reported survival probability is estimated as `P(A_H <= cutoff)`. The run uses 30 random seeds and 20,000 trials per seed and hop count. Confidence intervals are calculated across seed-level proportions.

## Important research scope

The delay-model script is **not a SeQUeNCe simulation**. It tests the arithmetic and sensitivity of the assumed delay distribution only.

The manuscript reports a separate SeQUeNCe baseline: 434,440 attempts, one generated resource, zero successful end-to-end links, one purged resource, and 0.00% usable entanglement. The original SeQUeNCe source, topology/configuration files, per-seed logs, and raw event logs were not included among the supplied files, so this repository does not claim to reproduce that run.

The paper's 16-hop route has a minimum modeled accumulated delay of `16 × 50 = 800 μs`. Consequently, with a 100 μs memory cutoff, survival through all 16 hops is impossible under the stated delay assumptions.

### Table V and Table VI

The supplied manuscript PDF has poorly rendered/malformed entries in Tables V and VI. A separate candidate table PDF includes numbers, but no original code or 30-seed output logs were supplied to verify them. This repository preserves those candidate values as supplied data but does **not** claim they have been independently reproduced or validated. Do not claim that PR outperforms B0/B1/B2 on the basis of the delay-model script.

## File map

- `src/`: executable analysis and result-audit scripts
- `data/raw/`: transcribed/supplied inputs
- `data/processed/`: generated outputs
- `figures/`: generated visualizations
- `docs/`: reproducibility notes

## Citation

Use the final published reference/DOI when available. Cite both the paper and this repository if the code contributes to a publication.
