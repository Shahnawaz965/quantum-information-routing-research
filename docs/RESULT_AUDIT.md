# Result audit of the supplied manuscript

## Consistent result

The manuscript describes a 16-link route with per-hop delay in the range 50–150 μs. The minimum accumulated delay is 16 × 50 = 800 μs; the mean is 1,600 μs; the maximum is 2,400 μs; and the standard deviation is approximately 115.5 μs. Since 800 μs exceeds the reported 100 μs hard cutoff, a resource traversing all 16 hops cannot survive under the assumed delay model. The reported baseline expiration is consistent with those assumptions.

## Table IV numerical cross-check

The supplied Table IV values mostly follow the expected CDF for the sum of independent Uniform(50,150) μs variables. However, the published Monte Carlo values cannot be reproduced exactly from the manuscript alone because the original random seeds and calculation script were not supplied.

For an independent theoretical cross-check with 600,000 total samples per hop count, selected supplied values differ from the exact CDF more than small rounding alone would explain:
- 3 hops, 200 μs: supplied 0.02173; theoretical CDF ≈ 0.020833.
- 12 hops, 1,000 μs: supplied 0.02164; theoretical CDF ≈ 0.022276.
- 16 hops, 2,000 μs: supplied 0.99977; theoretical CDF ≈ 0.999827.
These discrepancies do not by themselves prove the table is wrong; they do mean the exact random seed schedule, sampling convention, and aggregation/CI method should be checked against the original script before stating that the table has been independently reproduced. The included script generates a reproducible new run under the stated assumptions; its Monte Carlo values may differ from the supplied values.

## Reproducible versus non-reproducible evidence

- Table IV / Fig. 6 delay-model analysis: the model is clear and independently implementable, but the exact reported Monte Carlo realization is not reproducible without its original seed schedule.
- SeQUeNCe baseline: the paper reports 434,440 attempts, one generated resource, zero successful end-to-end links, one purged state, and 0.00% usable entanglement. The simulator source, topology/configuration, seeds, and raw event logs were not supplied; this repository records but does not independently reproduce that run.
- A separate supplied candidate-results PDF includes Tables V and VI values. The manuscript's rendered tables are malformed/overlapping and source logs are unavailable. These candidates are preserved for traceability but marked unverified. The identical policy values and mostly identical ablation values should be checked against the actual source CSV and code before being claimed as experimental evidence.

## Manuscript inconsistencies to verify before release

1. Equation (1) renders as f_r(A_r) = f_0 (-A_r/T_2), with the exponential operator apparently missing. The text describes exponential decay; visually verify the intended equation f_r(A_r) = f_0 exp(-A_r/T_2).
2. Table II appears to show 50–150 μs for the memory cutoff, while the baseline result and Table IV discussion use 100 μs. Keep 100 μs explicit as the baseline cutoff and identify 50–150 μs as the hop-delay range if that matches the actual run.
3. Page 6 renders the 16-hop 5th/95th age percentiles as approximately 1.41 μs and 1.79 μs. These appear to need ms (equivalent to about 1,410 and 1,790 μs); verify against the source output before correction.
4. Tables V and VI have malformed cell layout. The candidate values in the accompanying CSV are not independently validated.
5. Distinguish generation success probability per generation trial from aggregate success probability per transmission attempt, especially when five trials are launched per attempt.
6. The delay-model script is not the SeQUeNCe simulator. Do not present delay-model results as full network-simulator evidence.
