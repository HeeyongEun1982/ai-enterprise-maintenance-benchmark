# Enterprise Maintenance Requirements × AI Coding Benchmark Evaluation

Research materials for the manuscript **“Beyond Surface Metrics: Multi-Condition Requirements in Enterprise Maintenance and AI Coding Benchmarks”** (submitted for review at BenchSOC 2026). This repository provides the analysis source code, classification criteria, results, and supporting evidence for the study.

## Study scope

- Enterprise corpus: **2,925** Apache Fineract resolved issues, decomposed into **3,811** requirement units. The full raw Jira issue export is **not** included in this public package; summarized annotations and selected traceability excerpts are provided.
- Benchmarks: **944** AI coding tasks: SWE-bench Pro **v1 (731 tasks)**, PolyBench Java **165**, SWE-EVO **48**. We use the larger v1 task set to cover a broader range of tasks: v1 contains 731 tasks, compared with 642 in v2. The reported results describe v1; v2 changes both task membership and task contents. See [versioned datasets and release notes](https://huggingface.co/datasets/ScaleAI/SWE-bench_Pro).
- **3,446** task–criterion assignments against the frozen 18-criterion A/B taxonomy (six maintenance activities and twelve fulfillment conditions).
- E1: **1,177** matching pairs, mean Jaccard distance **0.8138** and **676** fully disjoint pairs. Matching controls native issue type and number of changed files exactly, and patch churn within a tolerance. This is not matched difficulty.
- E2: Corpus co-occurrence (e.g. Fineract B4–B2 phi ~**+0.430**, AI phi ~**−0.013**), **16** source-grounded business dependency relationships plus one technical reference, and four illustrative benchmark-oracle case studies. Co-occurrence is not causality and examples are not prevalence estimates.

### Follow-up on SWE-bench Pro v2

The NodeBB task remains in v2, but its explicit migration requirement was removed; the v1 specification-versus-test finding therefore does not transfer unchanged to v2. See the [submitted paper's goals and structural criteria](evidence/PAPER_GAP_AND_V2_REVIEW_PROTOCOL.md) and [structural review and counterexamples](evidence/V2_STRUCTURAL_REVIEW.md).

A subsequent [Proton Drive #0599 pipeline experiment](evidence/V2_PIPELINE_OMISSION_CASE.md) omitted a required root-key lookup: the published test bodies still satisfied 7/7 in a controlled adapter-based assertion replay because the encryption mock returned a fixed packet without checking its input key. A submission-omission control satisfied only 3/7, and an added key-binding assertion detected the lookup omission. [Reproduction code and results](ablation_study/proton_0599/README.md) are included. This is not an official Jest/container benchmark pass. The earlier batch-order-only interpretation remains withdrawn; the new evidence concerns a required intermediate operation and its downstream input binding. The original quantitative results remain v1 results.

## Start here

```bash
python -m pip install -r requirements.txt
python scripts/verify_all_claims.py
```

This runs **six targeted numerical/structural checks** over the included CSVs and evidence exports. Passing these checks does **not** establish semantic annotation validity, independent inter-annotator reliability, completeness of external evaluation harnesses, or license clearance.

For deeper checks with data already present:

```bash
python scripts/08_verify_gate2_master_plan.py
python scripts/09_verify_gate3.py
python ablation_study/nodebb_0030/inspect_nodebb_oracle.py
```

The NodeBB script examines the provided reference/ablated patches and the **supplied F2P test patch statically**. It does **not** run a benchmark container, measure a pass rate, or prove that other tests in the complete harness cannot detect migration errors. The developer migration file adds **44 LOC** and spans a **50-line unified-diff hunk**; these are not equivalent lengths.

### Re-generating selected outputs

The following use inputs **included here** (prefer a fresh clone or backup; generators overwrite their output files):

```bash
python scripts/03_generate_e1_matched_pairs.py
python scripts/04_generate_gate1_statistics.py
python scripts/09_generate_gate3_artifacts.py
```

`01_generate_baseline_tasks.py` reads the included original inputs under `data/inputs/` by default. The 944 task records, original family-mapping JSON and provenance manifest are included; see the [input inventory](data/inputs/README.md). To regenerate without overwriting the published CSV:

```bash
python scripts/01_generate_baseline_tasks.py --output-dir baseline-check
```

`02_generate_ab_long.py` reads its dedicated inputs under `data/02_generate_ab_long/`: the original codebook, assessment table and 944 task records. See the [script 02 input inventory](data/02_generate_ab_long/README.md). To regenerate without overwriting the published CSVs:

```bash
python scripts/02_generate_ab_long.py --output-dir ab-check
```

`06_reviewer_rebuttal_metrics.py` reads four packaged inputs, including the [2,925-record Fineract input](data/06_reviewer_rebuttal_metrics/README.md). Its keyword-based core/infra sets are computed but not used by the printed metrics. Manuscript-content checks are excluded from this package's verification scripts.

## Key files

| Path | Purpose |
|---|---|
| `data/framework-snapshot.json` | **Frozen 18-criterion codebook** (source of truth for names and boundaries) |
| `data/baseline_tasks.csv`, `data/ab_long.csv` | Task census, family metadata and coding decisions |
| `data/ab_all_evidences.csv` | Source quotations and coding rationales; not independently adjudicated labels |
| `data/e1_matched_pairs.csv` | E1 matching results |
| `data/gate3_*.csv` | Family tables, |B| distribution and pairwise phi values |
| `data/gate2_*.csv` | Selected dependency and test-assertion evidence |
| `data/fineract/summary.json`, `data/fineract/requirement-units.json` | Fineract summary and requirement-unit annotations |
| `data/fineract/gate2_raw_source_snippets.json` | Selected source-grounding excerpts, with original text/offsets |
| `data/ai_case_sources/` | Selected case specifications (third-party-origin text; see notices) |
| `ablation_study/nodebb_0030/` | NodeBB static patch-and-oracle comparison, **not a dynamic experiment** |
| `evidence/` | Reports and full evidence-table files; historical reports retain original paths and scope notes |
| `scripts/verify_all_claims.py` | Six numerical/structural checks (not a complete end-to-end regeneration) |

## The immutable codebook

The `name` field of `data/framework-snapshot.json` is authoritative; translations or paraphrases must **not** replace it in data exports. The B10–B12 labels are **service continuity/failure handling; interface/environment compatibility; user interaction**, not persistence retention, protocol conformance, or operational robustness.

| Code | Frozen original name |
|---|---|
| `A1` | Product Behavior and Business Rules |
| `A2` | Structure and Implementation Approach |
| `A3` | Testing and Quality Verification |
| `A4` | Execution and Operations |
| `A5` | Deployment, Versioning, and Environment Transition |
| `A6` | Development Process, Documentation, and Project Support |
| `B1` | Functional Outcomes and Input Conditions |
| `B2` | Numerical and Computational Accuracy |
| `B3` | Data Relationships and Integrity |
| `B4` | Temporal and Sequential Semantics |
| `B5` | State and Business Workflow |
| `B6` | Preservation of Existing Information and Behavior |
| `B7` | Concurrency and Transaction Boundaries |
| `B8` | Authorization and Protection |
| `B9` | Performance and Resource Utilization |
| `B10` | Service Continuity and Failure Handling |
| `B11` | Interface and Environment Compatibility |
| `B12` | User Interaction |


## Validity and transparency

A single primary investigator performed the semantic coding. There is **no substantiated blinded second coder or Cohen's kappa estimate** for this study. The earlier inter-annotator CSV and claimed κ figure were removed from this release because their independent collection/provenance was not established. See [annotation protocol](data/ANNOTATION_PROTOCOL.md).

Automated citation, string-offset and consistency checks confirm only their respective mechanical properties; they are not semantic adjudication. The four qualitative oracle case studies use **static analysis of specified artifacts**, not executed benchmarks, full-harness coverage, or measured resolved rates. Selected illustrative cases cannot support population-wide oracle omission rates or claims about real-world production failure prevalence.

## Source provenance, privacy and licensing

This release removes `data/fineract/fineract_resolved_issues.json` because the full source issue export contains upstream copyrighted content and email addresses; detailed source provenance is available from the official Apache Fineract project. The remaining excerpt-bearing files also require human clearance before a **public GitHub push**.

See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) and [LICENSE.md](LICENSE.md). **No blanket CC BY or MIT relicensing of upstream benchmark texts, original repository patches, or Jira descriptions is asserted.** SWE-bench Pro's dataset card explicitly states task content retains individual source-repository licenses; NodeBB itself is GPL-3.0. Authorship, redistribution rights and required notices remain a human review item before publishing. Never commit credentials or personal information.

## Citation and paper status

Manuscript: *Beyond Surface Metrics: Multi-Condition Requirements in Enterprise Maintenance and AI Coding Benchmarks* (BenchSOC 2026 submission). **Do not use an accepted-proceedings BibTeX entry unless and until acceptance/publication details are confirmed.** Cite original benchmark authors and dataset versions separately; see upstream dataset pages for authoritative references.
