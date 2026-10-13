# HealthConnect testing, refinement and validation

**Validation performed 11 October 2026.** This consolidates evidence against Week 7 requirements after the internship. It is not a backdated Week 7 submission, certification of assignment acceptance, or human collaboration record.

## Decision

Integrate Week 7 as a quality and validation layer around the existing candidate and final analytics. Do not retrain a new project or repeat the whole EDA. Week 6 already supplies model comparison, error analysis, sensitivity checks and local integration. Week 8 supplies descriptive analytics and a dashboard. Close technical gaps, preserve the historical record, and state unavailable external evidence explicitly.

## Requirement-to-evidence matrix

Status describes evidence coverage, not operational approval.

| Requirement | Existing evidence / current path | Status | Action and remaining need |
|---|---|---|---|
| Candidate model and test approach | `models/model_card.json`; `outputs/model/metrics/fold_definitions.csv` | Covered | Preserve candidate and chronological design |
| Classification metrics and confusion matrix | `outputs/model/metrics/reused_test_comparison.csv` | Covered | Independently recalculated from saved predictions |
| False positives / false negatives | `outputs/model/metrics/error_profiles.csv`; `segment_error_analysis.csv` | Covered | Add threshold-specific segment counts in validation outputs |
| Relevant segments | `outputs/validation/segment_diagnostics.csv` | Covered | Inspect gender, age, appointment type and seen/unseen IDs; no fairness claim |
| Feature suitability and timing | `src/healthconnect.py`; model card | Partly covered | Selected candidate excludes history, reminders and waiting time; real booking-time provenance remains unverified |
| Overfitting / generalisation | Temporal folds; `outputs/validation/generalisation_diagnostics.csv` | Partly covered | Compare train/internal/reused scores; fresh outcome window unavailable |
| Baseline comparison | `data/reference/`; model comparison CSV | Covered | Verify identical appointments and baseline probabilities |
| Meaningful improvement | Internal mean AUC 0.6481 vs 0.6416 | Partly covered | Smaller input dependency is concrete; statistically reliable predictive superiority is not established |
| Refinement and retest | Refinement table below; `validation_results.csv` | Covered | Fix actual path/schema defects, regenerate and recheck |
| Model suitability and business interpretation | Root README; model card; this report | Covered | Suitable for educational/local testing, not operational allocation |
| Cross-track testing | Historical AI-simulated ML Engineering record; current scoring and KPI parity tests | Partly covered | Local interfaces tested; no actual participant exchange or approval supplied |
| End-to-end local workflow | Data → model → serialised pipeline → scoring; data → analytics → dashboard | Covered | Executed technical workflow; dashboard does not call inference |
| KPI/dashboard correctness | `outputs/analytics/`; `scripts/validate_project.py` | Covered | Independent numerator/denominator and segment reconciliation; visible dashboard values checked |
| Fresh final validation | Original Week 7 test plan | Missing | Obtain later labelled data; do not relabel existing comparison records as fresh |
| Capacity and intervention validation | Hypothetical threshold 0.600 | Missing | Stakeholders must define workload and evaluate intervention outcomes |
| GenAI testing | No assistant implemented in this repository | Not applicable | Do not invent a chatbot or knowledge-base validation claim |

## Test results

The reproducible project validator reports **35 PASS, 3 BLOCKED, 1 NOT APPLICABLE**. The three blockers are fresh evaluation, verified human collaboration, and operational readiness. Filtering is not applicable to the static dashboard.

The first 17 interface tests were preserved from Week 6 and rerun. Extended checks cover duplicate columns, input container type, malformed dates/numerics, blank IDs, column order, Sunday warnings, and 5,000-record batch/chunk parity. The full-source batch includes cancellations only as a technical schema stress test; it does not extend model validity beyond the conditional binary population. Runtime is recorded as an observation, not an agreed SLA.

Machine-readable evidence:

- [Test cases: expected / actual / status / action / retest](../outputs/validation/validation_results.csv)
- [Run metadata](../outputs/validation/run_summary.json)
- [Original interface regression results](../outputs/validation/interface_results.csv)
- [Historical Week 6 results](history/week6_interface_results.csv)

## Actual defects and refinements

| Test / finding | Before | Action | Retest / result |
|---|---|---|---|
| Week 5 source path | Notebook expected capitalised CSV absent from `main`; reproducibility blocked on case-sensitive systems | Use one canonical lowercase source | Notebook executed; baseline probabilities match preserved reference within 1e-12 |
| Week 5 processed export | Destination directory never created | Create directory before export; generated data ignored in Git | Clean execution creates cohort successfully |
| Root dependency installation | Missing scikit-learn and joblib despite modelling notebooks | Consolidate core pinned requirements; separate optional notebook dependencies | Clean Python 3.12 environment installed successfully |
| Training-script launch location | Root resolution depended on current directory | Resolve repository from script path | Training reproduced from documented root command |
| Duplicate input columns | Actual reproduction raised pandas `TypeError` | Reject duplicate names explicitly with `ValueError` | Extended validation passes |
| Dashboard maintenance | Hard-coded KPI HTML and embedded images had no generation script | Build HTML from exported analytics; use shared chart files | Visible KPIs, payload and image paths reconcile |
| Ambiguous cohort terminology | Week 8 called Attended + No-Show “completed appointments” | Current dashboard/exports use “eligible appointments”; historical reports unchanged | Rates unchanged; denominator explicit |
| Fragmented evidence | Week 6 and Week 8 absent from `main`; README described Week 4 only | Consolidate branch content by purpose; retain unique historical reports | Current links and commands checked |

All model coefficients, candidate choice and threshold policy retain the existing experimental design. This consolidation does not tune on reused outcomes. Current predictions reproduce the preserved evidence; historical numerical reports remain applicable to their original experiments. Original PDFs are immutable historical documents, not current run instructions.

## Model interpretation

| Evidence population | N | ROC-AUC | Brier score |
|---|---:|---:|---:|
| Training (optimistic) | 3,682 | 0.6679 | 0.2305 |
| Pooled internal out-of-fold predictions (selection exposed) | 1,278 | 0.6497 | 0.2343 |
| Reused comparison | 799 | 0.6653 | 0.2304 |

Pooled internal AUC 0.6497 differs from mean fold AUC 0.6481 because aggregation differs. This modest train/internal gap does not show severe overfitting, but it cannot establish absence of overfitting or generalisation. The validation folds were used for model selection; the final comparison has been inspected before.

The candidate's baseline-relative fold AUC differences are approximately −0.0158, +0.0038 and +0.0314. Improvement is inconsistent across folds. On the reused comparison the candidate's AUC is lower by about 0.0025. Removing unreliable history inputs is the clearest justified refinement; no statistical superiority claim is made.

At threshold 0.50: TN 228, FP 184, FN 127, TP 260. At 0.60: TN 355, FP 57, FN 251, TP 136. This demonstrates the workload/recall trade-off. False positives are unnecessary follow-up in this illustrative scenario, not proof of clinical harm; false negatives are missed support opportunities, not measured intervention outcomes.

Five [calibration bins](../outputs/validation/calibration_bins.csv) and Brier scores are descriptive. Probabilities are not clinically calibrated. [Segment diagnostics](../outputs/validation/segment_diagnostics.csv) include sample sizes and positive/negative denominators at both thresholds. There are 702 comparison rows with IDs seen in training and 97 with unseen IDs; unreliable ID histories limit interpretation of both groups.

## Cross-track validation record

| Field | Evidence |
|---|---|
| Track connection | Data Science → ML Engineering-style local scoring interface; Analytics → Data Science cohort/interpretation |
| Input received | Existing Week 6 contract and saved model; Week 8 analytics exports |
| Output provided | Scoring outputs, explicit schema errors, KPI/segment checks and this evidence record |
| Test | Raw batch → engineered features → saved preprocessing/model → predictions; independent source totals → analytics → dashboard |
| Finding | Duplicate-column rejection unclear; dashboard was not regenerated by source script; terminology ambiguous |
| Action | Explicit schema error, dashboard generator and consistent cohort terminology |
| Retest | Local technical checks pass; evidence in `outputs/validation/` |
| Contribution | Reproducible handoff with clear input/output definitions and consistent interpretation |
| Human participation | Not supplied; the historical counterpart was AI-simulated |

A local integration test is not a substitute for the internship's requirement for a real exchange unless the programme explicitly accepts it. No acceptance is claimed.

## Remaining limitations and readiness

The repository is ready for portfolio review and local educational reproduction. Operational use remains unsupported. Fresh labelled data, trustworthy identity/history, cancellation eligibility, Sunday scheduling, timestamp provenance, group-performance criteria, staffing capacity, and a prospective intervention evaluation remain external requirements. No defects were fabricated to create an apparent improvement. New raw data was not invented or substituted.

## Execution environment and presentation checks

Core and optional notebook requirements installed in an isolated Python 3.12.14 environment. All four notebooks executed top-to-bottom in separate Python processes, their outputs were refreshed, and their notebook schemas validated. Native Jupyter kernel startup was attempted but blocked by the environment's socket permissions; a successful Jupyter session is not claimed.

Current Markdown file links and Python syntax were checked. All nine archived reports were compared byte-for-byte with their source branches. Static README/dashboard print previews and key figures were inspected. A live browser preview was unavailable because Chromium was missing and its download failed; responsive browser behaviour remains unverified. These environment limitations are separate from the 35-check project validator.

See [release_checks.json](../outputs/validation/release_checks.json) for the execution record. No remote write or deployment was performed.
