# Result audit of the supplied manuscript

## 1. Results consistent with the stated assumptions

The manuscript describes a 16-link route with each hop delay independently sampled from 50–150 μs. Therefore:
- minimum accumulated delay: 16 × 50 = 800 μs;
- mean accumulated delay: 16 × 100 = 1,600 μs;
- maximum accumulated delay: 16 × 150 = 2,400 μs;
- standard deviation: sqrt(16 × (100² / 12)) ≈ 115.5 μs.

The minimum 800 μs exceeds the 100 μs hard cutoff, so a generated resource traversing all 16 links cannot survive under the stated cutoff assumption. This supports the paper's diagnostic conclusion.

The supplied per-trial probability is approximately `1e-5 × 10^(-0.2) ≈ 6.31e-6`. Across 434,440 qubit trials, this gives an expected count of about 2.74 generated resources. Observing one is plausible for a stochastic low-yield process.

## 2. Table IV numerical cross-check

The supplied Table IV values broadly follow the expected cumulative distribution for a sum of independent Uniform(50,150) μs variables. Exact reproduction of the previously reported Monte Carlo values is not possible from the paper alone because the original seed schedule and source analysis script were not supplied.

For the theoretical CDF under the stated model:
- 3 hops, 200 μs: supplied 0.02173; theoretical CDF ≈ 0.020833.
- 12 hops, 1,000 μs: supplied 0.02164; theoretical CDF ≈ 0.022276.
- 16 hops, 2,000 μs: supplied 0.99977; theoretical CDF ≈ 0.999827.

These differences should be checked against the originating random seeds, aggregation method, and source CSV. They do not by themselves prove the supplied table is incorrect. The committed script performs a new, deterministic Monte Carlo realization; its output may differ slightly from the published realization.

A mathematical nuance: with 16 hops, survival is **impossible** for cutoffs below 800 μs, and **guaranteed** only for cutoffs at least 2,400 μs. A 1,000 μs cutoff has a very small but nonzero theoretical survival probability; a Monte Carlo estimate may report zero sampled successes.

## 3. Simulator provenance — significant issue

The manuscript states that the reported experiment was run using SeQUeNCe. A companion prototype found among the available working materials implements the baseline loop using **SimPy**, not SeQUeNCe. The repository now includes a clearly labelled SimPy baseline reconstruction; it must not be described as the SeQUeNCe implementation.

The original SeQUeNCe-specific source, topology/configuration files, random seed list, and raw event logs were not provided. Consequently, this repository independently reproduces the stated delay-model analysis and provides a transparent baseline reconstruction, but it does not yet independently reproduce the claimed SeQUeNCe run.

The original paper-reported counts—434,440 attempts, one generated resource, zero successful end-to-end links, one purged resource, 0.00% usable—are retained as reported values, not silently replaced by an output from the SimPy reconstruction.

## 4. Tables V and VI

A separately supplied candidate-results PDF contains policy and ablation values. The manuscript's rendered Tables V and VI have malformed/overlapping numerical cell layout, and no per-seed event logs or originating CSV/code were available to verify the candidates. They are preserved in `data/raw/supplied_table_V_VI_candidate_values.csv` with unverified provenance. Several policies have identical metrics and most ablations show the same results, which should be checked against the actual data-generation code before those values are used as evidence.

## 5. Other manuscript inconsistencies to verify

1. **Equation (1):** the submitted PDF appears to render the memory-decay formula without the exponential operator. The surrounding text suggests `f_r(A_r) = f_0 exp(-A_r/T_2)`; confirm against the editable manuscript.
2. **Table II:** the memory-cutoff entry appears inconsistent with the 100 μs baseline used in the result discussion. Clearly distinguish the memory cutoff from the 50–150 μs per-hop delay range.
3. **Percentile units:** the PDF appears to state approximately 1.41 μs and 1.79 μs for the 16-hop 5th/95th percentiles. These are likely intended as milliseconds (about 1,410 and 1,790 μs), but must be verified against the originating result file.
4. **Generation attempts:** clarify that 434,440 refers to individual qubit-generation trials, not 434,440 batches of five trials. Distinguish per-trial probability from per-batch probability.
5. **Path cost:** the `-ln(p_e F_e)` term and the normalized queue/latency/survival terms may be on different scales; explicitly explain normalization or scale the link term before adding it to normalized terms.

## 6. Scope of code in this repository

- `src/delay_model_sensitivity.py`: new Monte Carlo analysis for the delay-distribution assumptions.
- `src/baseline_diagnostic_simpy.py`: a runnable SimPy reconstruction of the baseline logic, not SeQUeNCe.
- `src/audit_paper_results.py`: arithmetic and provenance audit.
- CI runs the scripts and unit tests and uploads generated CSVs/figures as artifacts.

Until the original SeQUeNCe implementation and logs are available, do not claim that policy PR outperforms B0/B1/B2 based on this repository alone.
