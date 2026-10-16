# Third-party content and provenance

This package is a *research-derived* collection. License and attribution for upstream source material are **not** superseded by any license that may be assigned to the original analysis or scripts in this repository.

| Source | Where used | Upstream reference | Redistribution note |
|---|---|---|---|
| Apache Fineract | Issue identifiers, summaries, citations, requirement units and dependency excerpts | https://issues.apache.org/jira/projects/FINERACT and https://github.com/apache/fineract | Verify ASF issue-content terms and any personal data before redistributing full issue text. This public candidate omits the full `fineract_resolved_issues.json` original-issue export. |
| SWE-bench Pro **v1**, 731 tasks | Task metadata, evidence quotes, NodeBB example patch/test material | https://huggingface.co/datasets/ScaleAI/SWE-bench_Pro (select config `v1`) | Dataset card says task descriptions, patches, and tests retain the *respective original repositories' licenses*. MIT applies to evaluation tooling, not automatically to task content. |
| NodeBB | `ablation_study/nodebb_0030/` patch and test excerpts | https://github.com/NodeBB/NodeBB | NodeBB is GPL-3.0; preserve attribution and satisfy applicable GPL terms for any redistributed code or patch excerpts. Static inspection only. |
| PolyBench Java | Task metadata and annotations | See benchmark source and version used for the 165 selected tasks | Check the particular tasks/projects' license and permitted redistribution. |
| SWE-EVO | Task metadata and annotations | See benchmark source and version used for the 48 selected tasks | Check the particular tasks/projects' license and permitted redistribution. |

## Action before public push

1. Confirm license obligations for each included original code/diff/requirement excerpt and include required copyright notices and license text if redistributing.
2. Review `data/ab_long.csv`, `data/ab_all_evidences.csv`, `data/ai_case_sources/`, `data/fineract/gate2_raw_source_snippets.json` and `ablation_study/nodebb_0030/*.diff` for verbatim upstream text. Citation alone does not grant republication rights.
3. If rights cannot be confirmed, publish only the derived counts/tables/scripts and source identifiers, and link to the upstream originals rather than publishing verbatim source content.
4. This is a technical checklist, not a legal determination.
