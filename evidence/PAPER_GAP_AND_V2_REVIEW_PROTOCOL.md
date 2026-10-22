# Research Gap, Study Objectives, and v2 Review Protocol

Study: **Beyond Surface Metrics: Multi-Condition Requirements in Enterprise Maintenance and AI Coding Benchmarks**.

This document records the framing and selection criteria for the SWE-bench Pro v2 follow-up review, including corrections to early case interpretations. These are corrections to the follow-up analysis, not to the submitted paper.

The framing was checked against the 13-page submitted manuscript, historically named `BenchSOC_v3.pdf`; rendered pages 3, 5, 9, 10, and 12 were also inspected. That PDF is not included in this `git/` package. Section and table references below refer to the submitted version. The review did not modify it.

All links below refer to files in the current package.

## 1. Research gap

Sections 1.1–1.3 and 2.2–2.3, together with Table 1, identify a gap in describing maintenance completion through patch size, changed-file counts, repository navigation characteristics, or general issue types. These surface characteristics do not fully describe the conditions that must hold when maintenance is complete or their relationships.

The analytical unit is a **maintenance completion contract**: which state changes follow a development activity A, which conditions B must hold together, and which condition or operation requires a subsequent one. Condition counts, corpus-level co-occurrence, and source-grounded directional relationships are distinct properties.

A search for missing assertions alone would not capture the distinction from test-augmentation research such as UTBoost discussed in Section 2.2.

## 2. Study objectives and three analytical levels

| Level | Question and measurement | Interpretation scope |
| :--- | :--- | :--- |
| RQ1 / E1 | Do tasks with similar issue types, changed-file counts, and churn have the same completion-condition sets? How do condition counts differ? | Similar surface profiles need not imply identical semantic conditions. Matching does not establish equal difficulty. |
| RQ2a / E2 macro | How do temporal, numerical, and other conditions co-occur within each corpus? | Describe co-occurrence, conditional proportions, and higher-order co-presence; these do not establish direction, causality, or benchmark selection bias. |
| RQ2b / E2 micro | How do enterprise maintenance sources connect activities to conditions and conditions to subsequent obligations? | Describe 16 Fineract relationships with source evidence, rather than estimate directional relationship frequencies across a population. |

Sections 3.3, 5.3, 7.2, and 8 position the four benchmark-oracle cases as an application illustrating the evaluation implications of this structural analysis. General test-quality degradation or a benchmark-wide failure rate is not the primary measured outcome.

A change to the NodeBB example does not automatically invalidate statistics from the original v1 corpus. It also does not establish that those statistics remain unchanged for v2. See the [Gate 2 analysis report](Gate2_Verification_Report.md) for the packaged evidence.

## 3. What the NodeBB example illustrates

NodeBB #0030 in Section 5.3, Table 6, and Section 5.3.1 illustrates an explicit A5 -> B6 obligation:

1. **Functional change:** messaging permissions use allow/deny lists.
2. **Existing state:** users already have `restrictChat` settings and follow lists.
3. **Connected completion condition:** the upgrade must migrate existing information into the new allow list to preserve permission semantics. The new permission function alone does not satisfy that requirement.
4. **Developer implementation:** the reference patch includes local permission behavior and a separate database upgrade module.
5. **Inspected tests:** the added tests create users, set new lists directly, and check permission decisions. They do not directly assert the path from legacy data through migration to preserved behavior in the new feature.

The relevant distinction is between an explicit state-transition/preservation obligation and local functional assertions. A missing method-call-count assertion alone does not establish an equivalent mechanism. This static observation does not establish an official omission-pass result or prove that the complete runtime harness cannot detect the omission.

Packaged sources: [task specification](../ablation_study/nodebb_0030/nodebb_0030_spec.json), [reference patch](../ablation_study/nodebb_0030/nodebb_0030_developer_patch.diff), [test patch](../ablation_study/nodebb_0030/nodebb_0030_test_patch.diff), and [inspection instructions](../ablation_study/nodebb_0030/README_ABLATION_REPRODUCTION.md).

## 4. Criteria for structurally equivalent v2 cases

These criteria were defined for the follow-up review. Their numbering is not presented as part of the original submitted methodology.

- **G1 — Explicit requirement:** the v2 prompt, requirements, or interface directly requires transition or preservation of existing data/settings. Requirements found only in the reference patch or inferred from general operational practice do not qualify.
- **G2 — Dependency:** the source and implementation show an ordering or dependency between the local feature change and transition/preservation of existing state. Distinguish this from independent requirements listed together.
- **G3 — Implementation traceability:** connect the local feature and migration/preservation work to specific files and functions in the reference patch.
- **G4 — Test boundary:** inspect selected fail-to-pass (F2P), pass-to-pass (P2P), and execution scripts. Determine whether setup, call paths, and assertions check local functionality while bypassing the existing-state transition required by G1. Mock use alone does not establish a gap.
- **G5 — Counterevidence:** if existing tests, initialization paths, or additional verifier checks exercise migration/preservation, do not classify the case as an equivalent omission. Missing evidence leaves the result unresolved.

| Classification | Meaning |
| :--- | :--- |
| `strict_equivalent` | Evidence satisfies G1–G5. |
| `related_partial_gap` | Related assertion-scope differences without establishing the full equivalent structure. |
| `aligned_counterexample` | Tests exercise the dependency path. |
| `not_explicit` | The relevant requirement is not explicit. |
| `unresolved` | Available evidence or interpretation is insufficient. |

Related or unresolved cases are not combined with strict equivalents to claim that the same omission remains in v2.

## 5. Corrections to early case interpretations

- **Teleport #0521:** the test calls the migration function that creates a new remote CA. Missing existing/partially migrated setup did not establish the same mechanism as NodeBB's bypass of migration. It was classified as `related_partial_gap` and excluded as replacement evidence.
- **Proton Drive #0599:** tests call the migration action and check batch packets and error branches. The interpretation based on ordering or exact call counts was withdrawn as replacement evidence for NodeBB. The specification requires client request construction/transmission; separate server database migration persistence must not be added as an assumed requirement.

These cases can be relevant to the broader question, but the early observations did not verify structurally equivalent v2 replacements for NodeBB.

The [v2 follow-up review and additional findings](V2_FOLLOWUP_REVIEW.md) connect the initial review to the later Proton experiment and retain a brief interpretation-update history. The summary was reconstructed after deletion and is not a verbatim restoration of the original report. [Source metadata](../data/v2_followup_sources.json) and the [subsequent structural review](V2_STRUCTURAL_REVIEW.md) provide supporting records.

## 6. Effects of the version change

| Subject | Established scope or effect |
| :--- | :--- |
| Submitted v1 quantitative results | Remain results for the original analyzed corpus. The submitted PDF was not changed. |
| NodeBB explicit A5 -> B6 example | The migration requirement was removed from the v2 specification, so the same interpretation does not transfer unchanged. |
| Three-level distinction and reporting objectives | Remain the research framing. New empirical claims about v2 require separate evidence. |
| v2-wide statistics and dependency structure | This case review is not a full v2 reclassification or statistical recomputation. |

Follow-up decisions and sources are recorded in the [structural review](V2_STRUCTURAL_REVIEW.md) and [structured decision file](../data/v2_structural_review.json).

## 7. Subsequent intermediate-operation omission experiment

The [Proton Drive #0599 experiment](V2_PIPELINE_OMISSION_CASE.md) separately examines **root-key lookup -> re-encryption -> submission**. A variant omitting the key lookup satisfied all seven published test bodies in an adapter-based assertion replay (7/7).

This is different evidence from the withdrawn batch-order/call-count interpretation. It is not an official Jest or full benchmark grading pass; that execution scope is reported with the result.

The [reproduction package](../ablation_study/proton_0599/README.md) contains code and results. [Source metadata](../data/v2_pipeline_omission_sources.json) records provenance and outcomes. Controls include submission omission (3/7) and an added key-binding assertion that detects lookup omission (6/7 for the omission variant versus 7/7 for the reference).
