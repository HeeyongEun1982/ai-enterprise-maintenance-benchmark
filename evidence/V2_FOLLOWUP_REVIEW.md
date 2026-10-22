# SWE-bench Pro v2 Follow-up Review and Additional Findings

This document connects the initial case review with the additional finding from Proton Drive #0599. It summarizes preserved review records and subsequent experiments; it is not a verbatim restoration of the deleted initial document.

All links resolve within the current `git/` package. The [initial source metadata](../data/v2_followup_sources.json) records source provenance and collection scope. Task numbers such as #0599 refer to the original study's task identifiers.

## 1. Initial case review

The initial review examined the test scope of Teleport #0521 and Proton Drive #0599. Those observations alone did not establish structural equivalence with NodeBB #0030. Further investigation therefore focused on the connection between a required intermediate operation and downstream processing.

- **Teleport #0521:** the test actually calls the migration function. Differences in coverage of existing or partially migrated state do not by themselves establish the same intermediate-operation omission mechanism as NodeBB.
- **Proton Drive #0599:** beyond the initial observations about batch order and call counts, the follow-up separately examined the required key lookup and its connection to the re-encryption input.

Section 5 of the [research framing and review protocol](PAPER_GAP_AND_V2_REVIEW_PROTOCOL.md) records the interpretation update. The [structural review](V2_STRUCTURAL_REVIEW.md) documents the subsequent case assessment.

## 2. Additional Proton finding in v2

The Proton Drive #0599 specification requires **root-key lookup -> re-encryption using that key -> submission**.

In the additional experiment, omitting the root-key lookup still satisfied **7/7 published test bodies in an adapter-based assertion replay**. The encryption mock returns a fixed packet without checking its input key, so those assertions did not detect the missing connection between the required intermediate operation and the downstream input.

| Replay variant | Assertions satisfied |
| :--- | :---: |
| Reference implementation | 7/7 |
| Root-key lookup omitted | 7/7 |
| Submission-omission negative control | 3/7 |
| Reference with an added key-binding assertion | 7/7 |
| Key lookup omitted, with the same added assertion | 6/7 |

The added assertion detects the lookup omission. These values match the [source and result metadata](../data/v2_pipeline_omission_sources.json). The [experiment report](V2_PIPELINE_OMISSION_CASE.md) explains the method; the [reproduction package](../ablation_study/proton_0599/README.md) provides the code and result files.

## 3. Scope of the finding

The additional result identifies a gap between a required intermediate operation and the inspected assertions in this v2 Proton case. Execution used a limited assertion replay; it was not an official Jest or container benchmark grading run.

The initial batch-order/call-count interpretation is not used as evidence for this finding. Teleport was not confirmed as the same omission mechanism, and the submitted paper's v1 quantitative results were not changed.
