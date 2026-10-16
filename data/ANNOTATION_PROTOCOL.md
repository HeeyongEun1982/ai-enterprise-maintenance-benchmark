# Annotation and Evidence Protocol — verified scope

This repository contains the frozen 18-criterion annotation codebook and the exported classification records. It does **not** contain a verified independent second-annotator study. Annotation was performed by a single primary investigator; no Cohen's kappa, blind second coding, or consensus adjudication statistic is claimed.

## Data and scope

- `framework-snapshot.json`: original A1–A6 and B1–B12 names, descriptions, and scope boundaries; do not rename the codes.
- `ab_long.csv`: 3,446 task–criterion assignments over 944 AI benchmark tasks; includes classification rationale and source evidence.
- `ab_all_evidences.csv`: evidence-level excerpts that support individual decisions, not an independent gold-standard annotation.
- `fineract/summary.json` and `fineract/requirement-units.json`: enterprise issue and requirement-unit exports.
- `baseline_tasks.csv`: task-family and patch metadata for pairing and stratification.

## Annotation procedure and limits

1. Use the frozen `framework-snapshot.json` criteria and scope boundaries when interpreting each task or requirement unit.
2. Preserve original evidence quotations and source-field provenance; the evidence records help trace a classification but do not automatically establish that its semantic interpretation is correct.
3. Deduplicate at the task–criterion level for multi-label frequencies. The same task may carry multiple A and B criteria.
4. For E1, match native issue type and modified-file count exactly; use the recorded tolerance for patch churn. This does not match overall task difficulty.
5. For E2, distinguish statistical co-occurrence from directed requirements inferred from source language. Treat inferred dependencies separately from explicit and co-required relations.
6. For test-oracle cases, distinguish an explicit specification requirement from a developer-implemented or inferred property. The inspection is static, not a dynamic benchmark score.

## Reliability limitation

Source-string checking, offsets, and numerical re-computation can establish record-level consistency and textual provenance. They are **not** substitutes for independent semantic adjudication or inter-rater agreement. Users of this repository should report this limitation explicitly.

## Re-analysis

Run `python scripts/verify_all_claims.py` for the included summary checks. Additional cross-checks can be executed using the frozen dataset and the documented scripts in the repository README.
