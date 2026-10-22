# Gate 1 Verification Report: Dataset Preparation and Descriptive Statistics

Study: **Beyond Surface Metrics: Multi-Condition Requirements in Enterprise Maintenance and AI Coding Benchmarks**.

The original report was dated 2026-10-15. This edition updates its paths and descriptions to the current public package. Paths below are relative to the `git/` package root; clickable links are relative to this report.

## 1. Scope and packaged inputs

Gate 1 covers benchmark metadata, criterion assignments, criterion-level frequency comparisons, E1 matched pairs, and quotation traceability. Its principal outputs are:

- [Task metadata](../data/baseline_tasks.csv): 944 tasks.
- [Criterion assignments](../data/ab_long.csv): 3,446 unique task–criterion rows.
- [Individual evidence quotations](../data/ab_all_evidences.csv): 3,534 rows.
- [E1 matched pairs](../data/e1_matched_pairs.csv): 1,177 pairs.
- [Criterion-level statistical table](gate1_verified_table.md): 18 criteria.

The packaged source inputs are:

| Purpose | Input paths from the package root |
| :--- | :--- |
| Metadata extraction (script 01) | `data/inputs/maintenance18-ai944/comparison.json`, `data/inputs/se-ai-comparison/tasks/0001.json` through `0944.json` |
| Assignment and evidence export (script 02) | `data/02_generate_ab_long/framework-snapshot.json`, `data/02_generate_ab_long/table-view.json`, `data/02_generate_ab_long/tasks/0001.json` through `0944.json` |
| Fineract criterion counts | `data/fineract/summary.json` |
| Public criterion names and order | `data/framework-snapshot.json` |

See the input documentation for [script 01](../data/inputs/README.md) and [script 02](../data/02_generate_ab_long/README.md). Default execution uses packaged inputs; no external RAW5 folder is required. Script 02 exports existing assessments rather than performing new semantic classification. Its input snapshot is retained separately from the public snapshot.

## 2. Benchmark metadata

| Benchmark family | Tasks | Percentage |
| :--- | ---: | ---: |
| SWE-bench Pro v1 | 731 | 77.4% |
| PolyBench Java | 165 | 17.5% |
| SWE-EVO | 48 | 5.1% |
| Total | 944 | 100.0% |

`native_issue_types` preserves the source labels as a JSON array string. Among the 731 SWE-bench Pro tasks, 576 (78.8%) have multiple labels. `primary_issue_type` uses the first label for E1 matching; it does not replace the preserved full label list.

PolyBench Java supplies 165 task categories: Bug Fix 106, Feature 44, Refactoring 13, Testing 1, and Security 1. SWE-EVO does not supply the corresponding task-type metadata, so its 48 tasks are marked `unknown`. In total, 896 tasks have a usable primary type and 48 do not.

## 3. Criterion-level frequency comparisons

[Script 04](../scripts/04_generate_gate1_statistics.py) reads the Fineract summary, public codebook, benchmark task list, and assignment CSV. It computes two-sided Fisher exact tests, odds ratios, and approximate log-odds 95% confidence intervals, and writes `evidence/gate1_verified_table.md`.

The following table preserves the original report's numerical results. English criterion descriptions are provided here for readability; the packaged codebook retains its source names. Odds ratios compare Fineract with AI. The Bonferroni decision threshold is `0.05 / 18` (approximately 0.002778); confidence intervals are unadjusted 95% intervals.

| Code | Criterion (English description) | Fineract (N=2,925) | AI (N=944) | Odds ratio (95% CI) | Fisher p-value | Higher frequency after correction |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| **A1** | Product behavior and business rules | 1688 (57.71%) | 426 (45.13%) | 1.66 [1.43, 1.92] | $1.98 \times 10^{-11}$ | Higher in Fineract |
| **A2** | Structure and implementation approach | 987 (33.74%) | 572 (60.59%) | 0.33 [0.28, 0.39] | $9.83 \times 10^{-48}$ | Higher in AI |
| **A3** | Testing and quality assurance | 442 (15.11%) | 94 (9.96%) | 1.61 [1.27, 2.04] | $4.67 \times 10^{-5}$ | Higher in Fineract |
| **A4** | Execution and operations | 232 (7.93%) | 122 (12.92%) | 0.58 [0.46, 0.73] | $9.08 \times 10^{-6}$ | Higher in AI |
| **A5** | Deployment, version, and environment transitions | 470 (16.07%) | 60 (6.36%) | 2.82 [2.13, 3.73] | $9.34 \times 10^{-16}$ | Higher in Fineract |
| **A6** | Development process, documentation, and project support | 325 (11.11%) | 53 (5.61%) | 2.10 [1.56, 2.84] | $2.75 \times 10^{-7}$ | Higher in Fineract |
| **B1** | Functional results and input conditions | 942 (32.21%) | 315 (33.37%) | 0.95 [0.81, 1.11] | 0.5226 | No significant difference |
| **B2** | Numerical and calculation accuracy | 452 (15.45%) | 65 (6.89%) | 2.47 [1.88, 3.24] | $1.24 \times 10^{-12}$ | Higher in Fineract |
| **B3** | Data relationships and consistency | 600 (20.51%) | 214 (22.67%) | 0.88 [0.74, 1.05] | 0.1683 | No significant difference |
| **B4** | Temporal and ordering semantics | 520 (17.78%) | 86 (9.11%) | 2.16 [1.69, 2.75] | $3.27 \times 10^{-11}$ | Higher in Fineract |
| **B5** | State and business workflows | 465 (15.90%) | 131 (13.88%) | 1.17 [0.95, 1.45] | 0.1465 | No significant difference |
| **B6** | Preservation of existing information and behavior | 336 (11.49%) | 368 (38.98%) | 0.20 [0.17, 0.24] | $5.79 \times 10^{-72}$ | Higher in AI |
| **B7** | Concurrent execution and transaction boundaries | 64 (2.19%) | 42 (4.45%) | 0.48 [0.32, 0.71] | 0.0005 | Higher in AI |
| **B8** | Authorization and protection | 250 (8.55%) | 154 (16.31%) | 0.48 [0.39, 0.59] | $8.72 \times 10^{-11}$ | Higher in AI |
| **B9** | Performance and resource use | 129 (4.41%) | 83 (8.79%) | 0.48 [0.36, 0.64] | $9.59 \times 10^{-7}$ | Higher in AI |
| **B10** | Service continuity and failure handling | 83 (2.84%) | 87 (9.22%) | 0.29 [0.21, 0.39] | $1.50 \times 10^{-14}$ | Higher in AI |
| **B11** | Interface and environment compatibility | 975 (33.33%) | 391 (41.42%) | 0.71 [0.61, 0.82] | $7.85 \times 10^{-6}$ | Higher in AI |
| **B12** | User interaction | 390 (13.33%) | 183 (19.39%) | 0.64 [0.53, 0.78] | $9.10 \times 10^{-6}$ | Higher in AI |

Fifteen criteria meet the corrected significance threshold. B1, B3, and B5 do not. These comparisons describe criterion frequencies across the two corpora.

## 4. E1 matched-pair construction

[Script 03](../scripts/03_generate_e1_matched_pairs.py) uses `data/baseline_tasks.csv` and `data/ab_long.csv`. A pair is retained when:

1. Both tasks have the same `primary_issue_type`, excluding `unknown`.
2. Both have the same `patch_files_count`.
3. The absolute difference in `patch_loc_total` is at most `max(3, int(0.3 * max(LOC_1, LOC_2)))`.
4. At least one task has a B criterion.

The resulting CSV has 1,177 pairs: 714 within SWE-bench Pro and 463 within PolyBench Java. No cross-family pairs occur in this output; the script does not impose a separate same-family filter. There are 581 distinct participating tasks.

The mean Jaccard distance between B-criterion sets is 0.8138, the median is 1.0000, and the sample standard deviation is 0.2745. There are 676 disjoint pairs (57.43%). The CSV stores distances rounded to four decimal places.

A task can participate in multiple pairs, so these are dependent pair observations. The results describe differences in condition sets among tasks matched on the stated metadata; matching does not establish equal task difficulty.

## 5. Quotation traceability and multiple evidence records

The original preparation record identified 23 quotation mismatches across tasks 0028 (7), 0031 (5), 0033 (5), and 0034 (6). It attributed these to quotations appearing in the `requirements` field and to replacement of source newlines with spaces during CSV export.

The current export preserves source newlines using CSV quoting and records `evidence_source_field`. During this report update, all 3,446 representative quotations and all 3,534 individual quotations were checked as exact substrings of their recorded fields in `data/02_generate_ab_long/tasks/*.json`.

Of the 3,446 assignments, 58 have multiple evidence records, contributing 88 quotations beyond the first quotation per assignment:

- `data/ab_long.csv` stores one row per task–criterion combination, including `evidence_count`, the representative quotation, its source field, and the complete evidence list in `all_evidence`.
- `data/ab_all_evidences.csv` stores each quotation separately, including its evidence index and source field.

Quotation matching checks source traceability. The semantic classification remains available for review through the codebook, assessments, and quoted source material.

## 6. Regeneration and verification

Run these commands from the package root after installing `requirements.txt`:

```bash
python scripts/01_generate_baseline_tasks.py
python scripts/02_generate_ab_long.py
python scripts/03_generate_e1_matched_pairs.py
python scripts/04_generate_gate1_statistics.py
python scripts/verify_all_claims.py
```

Scripts 01–04 overwrite their corresponding outputs. Scripts 01 and 02 also accept `--output-dir` for comparison runs. All default input and output paths are resolved from the script location.

The historical script self-truncation issue is absent from the current script 01. The current scripts preserve multiple source labels and multiple evidence quotations. `verify_all_claims.py` checks selected counts and summary statistics; it does not rerun all source-quotation comparisons described above.
