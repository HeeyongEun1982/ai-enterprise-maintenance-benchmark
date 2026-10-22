# Structural Review of SWE-bench Pro v2 Cases and Additional Findings

Review date: **2026-10-21**. Study: **Beyond Surface Metrics: Multi-Condition Requirements in Enterprise Maintenance and AI Coding Benchmarks**.

This document combines the initial structural review with the subsequent Proton Drive #0599 experiment. The initial static review did not confirm a strict NodeBB-equivalent omission within its recorded scope. The later experiment supplied additional evidence of a required intermediate operation remaining untested by the inspected assertions in a controlled replay.

All local links resolve within the current `git/` package. Task numbers refer to the original study identifiers. The [initial structured review record](../data/v2_structural_review.json) preserves the static-review stage, including its original conclusion and `runtime_experiment` field. The later experiment is recorded separately in [Proton source and result metadata](../data/v2_pipeline_omission_sources.json); the initial JSON is not a consolidated statement of the later result.

## 1. Research framing

The review consulted the 13-page submitted manuscript, historically named `BenchSOC_v3.pdf`, which is not included in this package. Sections 1.3, 2.2–2.3, 3.3, 5.3, 7.2, and 8, together with Tables 1 and 6, frame the work as follows:

- **Gap:** surface task types, change size, and patch-discrimination tests do not fully describe the conditions and connections that constitute maintenance completion.
- **Objectives:** distinguish semantic differences and breadth in condition sets (RQ1), corpus-level co-occurrence (RQ2a), and source-grounded directional obligations (RQ2b).
- **Role of cases:** benchmark-oracle inspection illustrates the evaluation implications of that structural analysis.

A new case should therefore demonstrate a required transition or intermediate operation connected to downstream conditions, rather than merely a missing assertion. The [review protocol](PAPER_GAP_AND_V2_REVIEW_PROTOCOL.md) records the framing and G1–G5 selection criteria.

## 2. NodeBB structure and the v2 change

The NodeBB #0030 v1 dependency path is:

`existing restrictChat/follow state -> upgrade migration -> new allow list -> preserved permission semantics`

The v1 specification requires this path, and the reference patch includes a separate upgrade module. The inspected added tests instead set a new user's allow list directly and check permission decisions. This distinguishes preservation through legacy-state migration from local functional checks.

The v2 task retains the same identifier but removes the migration requirement and migration interface. The v1 migration-omission interpretation therefore does not transfer unchanged to v2. This affects the explicit A5 -> B6 example; it neither invalidates statistics computed from the original v1 corpus nor establishes those same statistics for v2.

The packaged [NodeBB specification and patch inspection](../ablation_study/nodebb_0030/README_ABLATION_REPRODUCTION.md) provides the v1 evidence. Version-specific source URLs and hashes are retained in the initial structured review record.

## 3. Initial review scope and method

- Retrieved 642 instructions from the official v2.0.0 tree `66f92766bba642462d4bbe5479e83f91f9211862`.
- Retrieved 83 keyword candidates using migration, legacy/existing data, idempotency, partial migration, rollback, and backward compatibility. Retrieval did not itself establish semantic relevance.
- Collected 108 artifacts for 18 tasks: 12 previous candidates plus six additional tasks, covering tests, grading settings, execution scripts, and reference patches. Separately retained NodeBB sources were also compared.
- Inspected explicit migration/preservation requirements, condition connections, implementations, and selected test paths. API renaming or configuration loading was distinguished from legacy-state migration.
- Recorded 15 decisions, including exclusions, aligned counterexamples, and unresolved cases. This was not semantic reclassification of all 642 tasks.
- Did not execute the complete harness or officially grade omission variants during this static stage. The subsequent Proton replay is described in Section 6.

The [initial decision file](../data/v2_structural_review.json) contains pinned URLs, hashes, selected tests, reasons, and scope limits.

## 4. Closest legacy-state candidate: Teleport #0670

Task ID: `instance_gravitational__teleport-1316e6728a3ee2fc124e2ea0cc6a02044c87a144-v626ec2a48416b10a88641359a169d99e935ff037`.

**Required path:** existing audit events must receive `CreatedAtDate` so that searches using the new date index also return legacy events. Writing the date field only for new events would not satisfy that completion contract.

**Implementation:** `lib/events/dynamoevents/dynamoevents.go` includes date-attribute storage, `indexTimeSearchV2`, `migrateDateAttribute`, and changes to `SearchEvents`.

**Selected v2 test:** `TestRFD24MigrateMakesLegacySearchable` is included in execution selection and F2P. It:

1. Stores three legacy events without the new date attribute.
2. Checks that date search returns zero events.
3. Calls the actual `migrateDateAttribute` function.
4. Checks that the same search returns three events.

The stateful in-process DynamoDB fake exercises **existing state -> actual migration -> new search result**. The absence of a cloud database does not make that path untested.

The named test is present in the stored v2 patch and absent from the stored v1 patch. This establishes addition of that test, not absence of all relevant checks from the complete v1 harness.

**Decision: `aligned_counterexample`.** The required state transition is structurally close to NodeBB, but this selected path is tested. It is not adopted as a migration-bypass omission case.

See the [pinned official task directory](https://github.com/scaleapi/SWE-bench_Pro-os/tree/66f92766bba642462d4bbe5479e83f91f9211862/v2/tasks/instance_gravitational__teleport-1316e6728a3ee2fc124e2ea0cc6a02044c87a144-v626ec2a48416b10a88641359a169d99e935ff037) and the source hashes in the initial decision file.

## 5. Candidate decisions and their scope

The Proton row explicitly includes the later result. Other rows retain the initial review decisions.

| Original task / identifier prefix | Decision or stage | Basis |
| :--- | :--- | :--- |
| Teleport #0039 `b5d8169f…` | Aligned counterexample | Repeated OSS migration calls and role/user/trusted-cluster mappings are checked. |
| Teleport #0521 `53814a2d…` | Related partial gap | The migration function is called. Missing existing-CA or partial-migration fixtures do not establish bypass of the entire migration path. |
| Proton Drive #0599 `2f2f6c31…` | Additional finding in assertion replay | Initial batch-order/call-count observations did not establish equivalence. A later root-key lookup omission still satisfied 7/7 published test bodies; Section 6 reports the distinct evidence. |
| qutebrowser #0691 `8d05f028…` | Aligned counterexample | A malformed legacy configuration is prepared and loading/migration error handling is checked. |
| Navidrome #0201 `5e549255…` | Related path tested | Album–genre state is prepared through storage and derived genre aggregation is checked; no separate legacy-migration omission was established. |
| Navidrome #0727 `3982ba72…` | Related path tested | Backup -> schema destruction -> restoration is selected, rather than only a local return-value check. |
| Navidrome #0088 `97434c17…`, #0095 `50015182…` | Migration obligation not established | Model/storage API changes do not justify inventing an additional legacy-record transition requirement. |
| OpenLibrary `910b0857…`, Flipt #0050 `f808b4dd…` | Outside the target structure | v2 focuses on response normalization or configuration/DSN compatibility; no separate legacy-state migration omission was established. |
| Flipt #0537 `9f8127f2…` | Unresolved | Migration test code exists; backend and image-internal checks were not fully inspected. |
| Teleport #0013 `c782838c…` | Unresolved | Conflicting specification statements about legacy aggregate preservation prevent a clear requirement–test mismatch determination. |
| Element-Web `9a31cd0f…` | Unresolved | Tests exercise upgrade API, progress, and dialog paths. Incomplete baseline context prevents asserting bypass of existing-member migration. |

The word “migration” in API-consumer changes, enum renaming, or component consolidation did not itself qualify a task as an existing-state transition/preservation case.

## 6. Additional Proton Drive #0599 verification

The follow-up examined a required value-dependency chain:

`root-link private-key lookup -> session-key re-encryption using that key -> migration submission`

The omission variant replaces `getLinkPrivateKey(abortSignal, share.shareId, share.rootLinkId, true)` with `Promise.resolve(undefined)`. The encryption mock returns a fixed packet without checking the key argument, so final packet assertions can remain satisfied despite the missing required lookup.

| Replay condition | Test bodies satisfied |
| :--- | :---: |
| Extracted reference migration | 7/7 |
| Root-key lookup omitted | 7/7 |
| Submission-builder omission negative control | 3/7 |
| Reference plus a key-binding assertion | 7/7 |
| Lookup omission plus the same assertion | 6/7 |

In the first normal omission case, the trace records zero root-key lookups and an undefined encryption key. An added assertion that encryption receives the expected session key and private key detects this omission.

This supplies additional v2 evidence of a required intermediate operation escaping the inspected assertions in an adapter-based replay. It is not based on the earlier batch-order/call-count interpretation, does not establish the full legacy-state G1–G5 classification, and is not an official Jest/container grading pass.

See the [experiment report](V2_PIPELINE_OMISSION_CASE.md), [reproduction code and results](../ablation_study/proton_0599/README.md), [source/result metadata](../data/v2_pipeline_omission_sources.json), and [follow-up overview](V2_FOLLOWUP_REVIEW.md).

## 7. Updated conclusion for the public analysis

The submitted paper and original quantitative results concern v1. NodeBB's explicit migration requirement was removed in v2, so the original specification-versus-test observation does not transfer unchanged to that task. Teleport #0670 provides a positive example that tests a legacy-state migration path.

The initial static review did not confirm a strict equivalent within its recorded scope. Subsequently, Proton Drive #0599 provided an additional intermediate-operation/input-binding case: root-key lookup omission satisfied 7/7 published test bodies in a controlled assertion replay, and a key-binding assertion detected it. Teleport #0521 remains a related partial-scope observation rather than an equivalent omission case.

These findings support reporting the particular v2 case and its measured execution scope. They do not establish that every v1 issue is resolved in v2, that all v1 statistics remain the same in v2, or a v2-wide omission rate. The submitted paper and v1 classification data were not changed.
