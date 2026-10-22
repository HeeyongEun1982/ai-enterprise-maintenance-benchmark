# Inputs for baseline task generation

These are the original local study inputs used by
`scripts/01_generate_baseline_tasks.py`, copied without content changes.

| Path | Purpose |
|---|---|
| `maintenance18-ai944/comparison.json` | Original task index and benchmark-family mapping |
| `se-ai-comparison/tasks/0001.json`–`0944.json` | 944 task records, including task metadata and reference patches |
| `se-ai-comparison/manifest.json` | Original task ordering, source references and recorded hashes |
| `PROVENANCE.json` | Copy inventory with original workspace-relative paths, byte lengths and SHA-256 hashes |

The original manifest is preserved unchanged; its path fields describe the
original workspace layout. Paths to these packaged files are relative to this
input directory as shown above.

From the package root:

```bash
python scripts/01_generate_baseline_tasks.py --output-dir baseline-check
```

No RAW5 directory is needed for this script. `--input-dir` can select another
directory with the same layout. The legacy `--raw5` option remains supported.

Scope: SWE-bench Pro **v1** 731 tasks, PolyBench Java 165, SWE-EVO 48.
Regeneration on 2026-10-21 reproduced all values in the published 944-row
`data/baseline_tasks.csv`; only line-ending bytes differ.

This input set covers script 01. Script 02 has a separate input directory at
`../02_generate_ab_long/`, including its codebook, assessment table and task records.
Upstream task contents retain their original source licenses; see
`../../THIRD_PARTY_NOTICES.md`.
