# Script 06 Fineract input

`fineract_issues.json` is an unchanged copy of the 2,925-record local source:
`comparison/raw2-review-20261014/Task_1.2_Fineract_Mapping/fineract_10_concerns_mapped.json`.

Script 06 uses only `key`, `summary` and `description` for its financial-keyword
screening. Existing concern-mapping metadata in the copied file is not used.
The resulting core/infra sets are currently not used by the printed metrics.

`PROVENANCE.json` records the source path, byte size and SHA-256. The copy matches
the source byte for byte, has 2,925 unique issue IDs, and contains every issue ID
referenced by the packaged Fineract annotation summary.

All four script inputs are inside the public-package working directory:

- `data/06_reviewer_rebuttal_metrics/fineract_issues.json`
- `data/fineract/summary.json`
- `data/baseline_tasks.csv`
- `data/ab_long.csv`

Paths are resolved relative to the script's package root. No external research
folder is required. Run from the package root with:

```bash
python scripts/06_reviewer_rebuttal_metrics.py
```

This script prints metrics to the console; it does not write a results file.
Upstream source text retains its source licensing; see `../../THIRD_PARTY_NOTICES.md`.
