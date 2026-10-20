# Simulating Information Routing in Quantum Networks

Research-code companion to **“Simulating Information Routing in Quantum Networks.”**

## Repository contents

- `src/delay_model_sensitivity.py`: Monte Carlo survival sensitivity for hop counts 1–16 and cutoff values of 100, 200, 500, 1,000, 2,000, and 3,000 μs.
- `src/baseline_diagnostic_simpy.py`: runnable reconstruction of the supplied baseline model, generating summary CSVs, resource-event logs, hop-delay samples, and topology/results figures. This is **SimPy**, not SeQUeNCe.
- `src/audit_paper_results.py`: arithmetic checks for the 16-hop, 100 μs-cutoff conclusion.
- `tests/test_delay_model.py`: tests for generated outputs and mathematical bounds.
- `data/raw/`: supplied baseline parameters, Table IV values, and candidate Table V/VI values with provenance notes.
- `docs/RESULT_AUDIT.md`: numerical audit and manuscript inconsistencies.
- `.github/workflows/reproducibility.yml`: CI workflow that runs the scripts, tests, and uploads generated artifacts.

## Setup and run

Python 3.10+ is recommended.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/delay_model_sensitivity.py
python src/baseline_diagnostic_simpy.py --seed 2026 --horizon-s 10
python src/audit_paper_results.py
python -m unittest discover -s tests -v
```

The delay model writes `data/processed/table_iv_reproduced.csv` and `figures/delay_model_survival.png`. The baseline reconstruction writes summary/resource CSVs and figures under `data/processed/` and `figures/`. GitHub Actions uploads generated files as an artifact after each CI run.

## Model definitions

For a path with H hops, the delay sensitivity model samples independent hop delays:

`D_i ~ Uniform(50, 150) μs`

The accumulated age is `A_H = sum(D_i)`; survival is estimated as `P(A_H <= cutoff)`. It uses 30 seed-level batches of 20,000 trials per hop count, and reports the mean and a Student-t 95% confidence interval across the 30 seed-level estimates.

The baseline diagnostic model uses 15 intermediate routers (16 links), 10 km links, 0.2 dB/km attenuation, five generation trials per attempt, a 100 μs hard cutoff, and a 10 s simulated horizon.

## Important simulator distinction

The manuscript states that the main result was obtained using SeQUeNCe. The companion baseline script found in the working materials uses **SimPy**, a separate discrete-event process library, and cannot substantiate a claim that the run was executed in SeQUeNCe. This repository labels the script accurately as a baseline reconstruction, not as SeQUeNCe source code. The original SeQUeNCe model source, topology/configuration files, RNG seeds, and raw event logs remain unavailable in the supplied materials.

The manuscript reports 434,440 qubit attempts, one generated resource, zero successful end-to-end links, one purged resource, and 0.00% usable entanglement. The SimPy reconstruction's random output may differ from these recorded values and must not overwrite them as though it were the original run.

## Core numerical conclusion

For 16 hops, the minimum possible accumulated delay is `16 × 50 = 800 μs`, the mean is 1,600 μs, and the maximum is 2,400 μs. Therefore a 100 μs cutoff cannot allow a resource to survive the entire path under the assumed delay model.

## Tables V and VI: provenance warning

The supplied manuscript has malformed/incomplete rendering of Tables V and VI. A separate supplied table PDF contains candidate metrics, but the original per-seed logs and source implementation are not available to verify them. Candidate values are preserved in `data/raw/supplied_table_V_VI_candidate_values.csv` as unverified source data. Do not claim that PR outperforms B0/B1/B2 based on those numbers unless they are verified from the actual run logs.

## Paper file

The repository currently contains analysis code and data transcribed from the supplied paper, but does **not** contain the original paper PDF as a tracked binary file. Add the final author-approved PDF to `paper/` before treating this as a complete paper-plus-code archive.

## Citation

Use the final bibliographic reference and DOI when available. Cite the paper and this repository when the code contributes to a publication.
