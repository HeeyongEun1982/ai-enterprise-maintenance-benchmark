# GitHub publication checklist (2026-10-16)

## Completed in this edited copy

- [x] Removed unsubstantiated second-annotator agreement dataset and κ script from the distributable package; replaced `ANNOTATION_PROTOCOL.md` with a single-coder methodology and explicit limitation.
- [x] Corrected README's B10–B12 naming against `data/framework-snapshot.json` without changing the frozen codebook or analysis data.
- [x] Rebased local scripts to the package layout; source builders requiring external RAW5 inputs now take `--raw5` explicitly.
- [x] Renamed misleading `eval_harness.py` to `inspect_nodebb_oracle.py`; explicitly documented static F2P inspection only.
- [x] Removed the bulk Fineract issue-source JSON containing email addresses. The exported summary/derived requirement units and selected evidence are retained.
- [x] Added `.gitignore`, `requirements.txt`, and third-party provenance/rights warnings.
- [x] Removed fake accepted-proceedings BibTeX entry and blanket relicensing claims from README.
- [x] Verified frozen E1 and Gate 2 regenerated CSVs unchanged; Gate 3 regenerated CSVs now byte-identical after normalizing line endings.

## Manual approval still required before public upload

- [ ] Decide the repository's **actual author-owned license** and supply correct copyright/attribution; `LICENSE.md` deliberately does NOT grant a license.
- [ ] Confirm redistribution rights for the included original upstream code diffs, benchmark requirements/test excerpts and `ai_case_sources` JSONs; see `THIRD_PARTY_NOTICES.md`. If not clear, replace those third-party excerpts with upstream URLs and derived identifiers.
- [ ] Confirm no unpublished, private, or personally identifying source is embedded in evidence CSV/JSON/MD excerpts. A basic email-pattern scan passed for this edited copy; this is **not** comprehensive PII or secret scanning.
- [ ] Confirm paper v0.5 matches the immutable codebook, numerical tables, and static-oracle scope. Updating the repository does **not** correct the manuscript.
- [ ] Optional: test regeneration from the independently obtained original RAW5 tree; it is not included in this release.

## Verification commands (from repository root)

```bash
python -m pip install -r requirements.txt
python scripts/verify_all_claims.py
python scripts/08_verify_gate2_master_plan.py
python scripts/09_verify_gate3.py
python ablation_study/nodebb_0030/inspect_nodebb_oracle.py
```

All four checks ran successfully against the files in this edited copy. No dynamic full-harness test was executed.
