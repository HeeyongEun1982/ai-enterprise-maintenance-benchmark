# Gate 2 Verification Report: Requirement Relationships and Evaluation Scope

Study: **Beyond Surface Metrics: Multi-Condition Requirements in Enterprise Maintenance and AI Coding Benchmarks**.

This English edition updates the historical v0.4.4 report to the current public package. Paths in code spans are relative to the `git/` package root; links are relative to this report. The report describes source-grounded requirement relationships and four illustrative benchmark cases.

The central proposition is that technically appropriate tests within an intended scope can still omit interconnected conditions relevant to enterprise maintenance. Corpus co-occurrence, source-grounded relationships, and test-assertion scope are examined separately.

## 1. Source grounding and paired clauses

The dependency records retain the source quotation, its character offset, and, where needed, a paired consequence quotation. This makes the connection between an operation and its required consequence available for inspection.

- **DEP-01 (FINERACT-2338, A1 -> B4):** the permission to backdate changes to paid installments (position 261) is paired with the requirement to reverse and replay interest from the applied date (position 559).
- **DEP-05 (FINERACT-753, A1 -> B4, B2):** reversal of a deposit (position 1494) is paired with recalculation of daily balances and reversal of the charge transaction (position 1532).
- **DEP-07 (FINERACT-2836, B7 -> B6):** independent installment transactions (position 853) are paired with preservation of successfully committed installments (position 1016). This is classified as explicit.
- **DEP-08 (FINERACT-2836, B7 -> B3):** the data-consistency rationale for independent transactions is classified separately as inferred.
- **DEP-09 (FINERACT-2836, A4 -> B6):** rerunning the job resumes at the first unpaid installment without collecting committed installments again (position 2293). The recorded direction is operational rerun to preservation of prior results.

The stored quotations and positions can be checked against [the packaged Jira source descriptions](../data/fineract/gate2_raw_source_snippets.json). Positions are Python string character offsets, not byte offsets.

## 2. Artifact generation and analytical review

[Script 05](../scripts/05_generate_gate2_artifacts.py) exports manually authored analysis records into four CSV files. It does not extract relationships automatically from natural language. Regeneration reproduces the encoded records; source review uses the quoted text, codebook, classification rationale, and boundary notes.

The 16 core relationships have the following classifications:

| Classification | Count | Interpretation |
| :--- | ---: | :--- |
| Explicit Dependency | 12 | A sequence, trigger, consequence, or preservation constraint is directly stated in the source. |
| Co-required | 2 | Conditions are required together; their listing alone does not establish a causal direction. |
| Inferred Dependency | 2 | The relationship includes a researcher interpretation grounded in domain or architecture principles. |

DEP-SUPP-01 (FINERACT-977) is a separate technical call-graph reference and is excluded from the 16 business relationships.

## 3. Fineract relationship records

The following table uses the current [dependency CSV](../data/gate2_dependencies.csv). It preserves issue status at collection, classification, relation codes, exact quotation text, and recorded positions. The examples include resolved, in-progress, and open issues; requirement evidence from an open issue is not evidence that an implementation was completed.

| ID | Issue | Status | Classification | Recorded relation | Source quotation and position |
| :--- | :--- | :--- | :--- | :--- | :--- |
| DEP-01 | FINERACT-2338 | Resolved | Explicit Dependency | A1 -> B4 | Backdate can be done on already paid Installments as well (pos: 261)<br>Paired: Installments paid Interest amount will be reverse replayed as per the new Interest rate from the applied date (pos: 559) |
| DEP-02 | FINERACT-2338 | Resolved | Explicit Dependency | B4 -> B2 | Repayment schedule will be recalculated with New EMI and Interest from the Interest applied schedule date (pos: 325) |
| DEP-03 | FINERACT-2338 | Resolved | Explicit Dependency | B2 -> B6 | No of Installments will remain the same, only EMI and Interest would get affected (pos: 843) |
| DEP-04 | FINERACT-2338 | Resolved | Explicit Dependency | B4 -> B3 | If the repayment that was made before the charge-off is reversed and replayed due to backdated Interest modification,then the accounting entry of the reversed transaction and replayed transaction should follow *standard accounting rules and not charge-off accounting rules* (pos: 1005) |
| DEP-05 | FINERACT-753 | Resolved | Explicit Dependency | A1 -> B4, B2 | now reverse the deposit of 500 . (pos: 1494)<br>Paired: system will recalculateDailyBalances and reverse the charge transaction on this section of the code (pos: 1532) |
| DEP-06 | FINERACT-753 | Resolved | Explicit Dependency | B4 -> B3, B6 | now since the new charge created does not have the charged paid by object in the table "  m_savings_account_charge_paid_by" recalculating the account balance becomes wrong (pos: 2160) |
| DEP-07 | FINERACT-2836 | In Progress | Explicit Dependency | B7 -> B6 | Each due savings-charge installment is processed in an independent transaction. (pos: 853)<br>Paired: A successfully collected installment remains committed regardless of the outcome of another installment. (pos: 1016) |
| DEP-08 | FINERACT-2836 | In Progress | Inferred Dependency | B7 -> B3 | Each due savings-charge installment is processed in an independent transaction. (pos: 853) |
| DEP-09 | FINERACT-2836 | In Progress | Explicit Dependency | A4 -> B6 | Re-running the job resumes from the first unpaid installment without collecting previously committed installments again. (pos: 2293) |
| DEP-10 | FINERACT-2836 | In Progress | Co-required | A1, B5 -> B7, B6 | the job is not marked as failed solely because of the insufficient balance (pos: 1718) |
| DEP-11 | FINERACT-2930 | In Progress | Explicit Dependency | A1 -> B4 | The loan is replayed from the earlier of the original and new transaction dates. (pos: 2147) |
| DEP-12 | FINERACT-2930 | In Progress | Co-required | B4 -> B3, B2, B5 | The schedule, balances, allocations, accruals and loan status (e.g. closed ↔ active, overpaid) are recalculated correctly. (pos: 2228) |
| DEP-13 | FINERACT-2930 | In Progress | Explicit Dependency | A1 -> B3 | The new transaction stays linked to the same loan charge (LoanChargePaidBy / charge relation). (pos: 3368) |
| DEP-14 | FINERACT-2930 | In Progress | Explicit Dependency | A1, B3 -> B2 | counting the reversed original as available again (pos: 3561) |
| DEP-15 | FINERACT-2930 | In Progress | Inferred Dependency | B3, B2 -> B6 | Journal entries are reversed for the original transaction and posted for the new one, using the correct accounts for that transaction type. (pos: 2357) |
| DEP-16 | FINERACT-2934 | Open | Explicit Dependency | A5 -> B6 | For installations that already configured both rows, the effective behaviour does not change. (pos: 1527) |
| DEP-SUPP-01 | FINERACT-977 | Resolved | Technical Call Graph | A2 -> B1 | updateAmountsBasedOnCurrentEarlyPayments (AbstractLoanScheduleGenerator.java:640) (pos: 239) |

The full CSV also provides relationship synthesis and boundary/preservation notes for each record. The core records contain 19 quotations including paired consequences; the supplementary reference brings the total to 20.

## 4. Four benchmark comparison cases

### 4.1 Roles and specification boundaries

- **NodeBB #0030 / FINERACT-2934 — direct functional comparison:** both concern migration of configuration while preserving existing behavior. The v1 NodeBB specification requires migration of existing settings and safe repeated execution. The inspected added tests exercise messaging permissions using new settings directly.
- **Element-Web #0139 / FINERACT-2930 and FINERACT-2338 — scope comparison:** mocked event combinations test unread-message decisions. Financial replay and messenger unread-state calculation have different purposes. Inferred IndexedDB or server consistency conditions are not treated as omitted explicit requirements.
- **RocketMQ #0819 / FINERACT-2836 — concurrency-level comparison:** the Java test exercises shared-memory atomicity in one JVM; the Fineract requirements concern independent business transactions, partial failures, committed results, and rerun behavior. Two-phase commit, network partitions, and distributed-broker obligations are not added to the Fineract source requirements.
- **Navidrome #0495 — aligned positive case:** the test patch includes SQLite backup/restoration and backup retention/pruning assertions. It illustrates concrete stateful verification at database-schema and file levels.

The current mapping is:

| Axis | Role | Domain | Fineract anchor | AI task | Selection rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Axis-1 | Direct Functional Comparison | Configuration Data Migration and Idempotency | FINERACT-2934 (Open / Unresolved) | 0030 | The problem statement explicitly requires a batch upgrade script (src/upgrades/4.3.0/chat_allow_list.js) to migrate accounts with restrictChat enabled to chatAllowList, including safe repeated execution. This provides a direct within-task comparison between configuration-migration requirements and evaluation-harness assertion scope. |
| Axis-2 | Evaluation Scope and Abstraction Gap | Temporal State Transitions and Backdated Recalculation | FINERACT-2930 (In Progress) / FINERACT-2338 (Resolved) | 0139 | The task recalculates unread badges when read receipts are reordered across room and thread timelines. Its development purpose differs from backdated financial-ledger recalculation; it illustrates the localized in-memory state decisions measured by mock-based unit tests. |
| Axis-3 | Concurrency and Isolation-Level Hierarchy | In-Process Thread Safety versus Business-Transaction Partial-Failure Isolation | FINERACT-2836 (In Progress) / FINERACT-753 (Resolved) | 0819 | The task includes a high-load thread-safety stress test that makes StatsItemSet insertion atomic with putIfAbsent. It illustrates the distinction between atomic operations within one JVM and independent isolation and commit preservation in enterprise business transactions. |
| Axis-4 | Positive Benchmark Evaluation Case / Aligned Counterexample | Database-Engine Backup, Schema Restoration and Retention Pruning | Database Infrastructure Backup & Disaster Recovery Operational Baseline | 0495 | The only task among the 944 analyzed tasks that tests persistent database operations using a running engine to create SQLite backups, restore after destructive DDL deletion, and enforce backup-count retention and pruning of old files. |

### 4.2 Recorded assertions and evaluation scope

These are assertion excerpts recorded in the [harness evidence CSV](../data/gate2_harness_evidence.csv). They are excerpts, not complete runnable test files.

| Task | Test files | Assertion excerpt | Evaluated scope | Boundary |
| :--- | :--- | :--- | :--- | :--- |
| 0030 | test/messaging.js, test/user.js | await assert.rejects(Messaging.canMessageUser(uid2, uid1), { message: '[[error:chat-restricted]]' }); | Server-side leaf permission checks at chat-message submission time (in-memory permission gating). | No execution experiment modified or removed the harness's complete regression tests. The evidence shows that the added F2P unit-test assertions focus on leaf permission branches. |
| 0139 | test/Unread-test.ts, test/test-utils/threads.ts | expect(doesRoomHaveUnreadMessages(room)).toBe(true); expect(doesRoomHaveUnreadMessages(room)).toBe(false); [Mock: mocked(haveRendererForEvent).mockReturnValue(true); thread.initialEventsFetched = true;] | Unread-badge decisions over synthesized room/thread event hierarchies held in memory (in-memory state-transition logic). | Mocking is an appropriate unit-isolation technique. This case identifies the boundary of the measured capability rather than a defect in the individual evaluation. |
| 0819 | common/src/test/java/org/apache/rocketmq/common/stats/StatsItemSetTest.java | assertEquals(20000L, test_unit().longValue()); [Framework: executor = new ThreadPoolExecutor(100, 200, 10, TimeUnit.SECONDS, new ArrayBlockingQueue<Runnable>(10000)); for (int i = 0; i < 50; i++) ...] | Thread safety of shared-memory data structures within a single JVM (in-process multithreaded race conditions). | A strong thread-safety test that illustrates the distinction between single-process memory concurrency and business-transaction isolation. |
| 0495 | db/backup_test.go | Expect(isSchemaEmpty(Db().WriteDB())).To(BeFalse()); Expect(len(timesDecreasingChronologically) - pruneCount).To(Equal(expected)); Expect(err).To(MatchError(os.ErrNotExist)); [Setup: path, err := Db().Backup(ctx); ExecContext(ctx, 'DELETE FROM sqlite_master ...'); Expect(isSchemaEmpty(Db().WriteDB())).To(BeTrue());] | SQLite backup-file creation, schema presence after destructive operations and restoration, and enforcement of backup-file retention pruning. | An aligned counterexample based on the test configuration and observed assertions, consistent with the Gate 1 labels (A4, B1, B4, B8, B10; B6 excluded). |

Full case conclusions and boundaries are stored in [the verdict CSV](../data/gate2_case_verdicts.csv). The Element, RocketMQ, and Navidrome original task records are packaged under [data/ai_case_sources/](../data/ai_case_sources/); NodeBB sources are listed in Section 7 below.

## 5. Corpus-level co-occurrence and family profiles

Co-occurrence counts and phi correlations describe whether criteria occur together within an issue or task. Directional relationships require the source-grounded analysis above; phi does not establish causal direction or absolute statistical independence.

The following values come from [the current correlation CSV](../data/gate3_phi_correlation_matrix.csv). Each p-value is a within-corpus Fisher exact test of the criterion pair, not a test of the difference between the two phi coefficients.

| Pair | Fineract co-occurrence | Fineract phi | Fineract Fisher p | AI co-occurrence | AI phi | AI Fisher p |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| B4-B2 | 254 | 0.43 | 2.76e-95 | 5 | -0.013 | 0.825 |
| A1-B4 | 471 | 0.309 | 1.71e-72 | 42 | 0.024 | 0.496 |
| A1-B2 | 440 | 0.343 | 3.2e-98 | 34 | 0.039 | 0.246 |
| A1-B3 | 538 | 0.329 | 1.56e-80 | 115 | 0.094 | 0.00486 |
| B4-B3 | 138 | 0.069 | 0.000252 | 22 | 0.022 | 0.501 |
| B4-B6 | 84 | 0.068 | 0.000457 | 28 | -0.042 | 0.246 |
| B2-B3 | 189 | 0.226 | 5.62e-30 | 14 | -0.007 | 1 |
| B2-B6 | 64 | 0.036 | 0.0545 | 19 | -0.054 | 0.113 |
| B3-B6 | 89 | 0.053 | 0.00503 | 63 | -0.106 | 0.00108 |
| B7-B6 | 8 | 0.005 | 0.696 | 14 | -0.025 | 0.519 |
| B7-B3 | 20 | 0.04 | 0.0407 | 7 | -0.031 | 0.451 |

For B4–B2, Fineract has 254 co-occurrences and phi +0.430; AI has 5 co-occurrences and phi -0.013. The AI count is 0.53% of all 944 tasks. These are different observed co-occurrence patterns; the near-zero AI coefficient does not demonstrate complete decoupling.

Family-specific frequencies and B-criterion distributions are available in [the stratified metrics](../data/gate3_stratified_family_metrics.csv) and [the complexity distribution](../data/gate3_coupling_complexity.csv). Mean B-criterion counts are 2.4733 for SWE-bench Pro, 1.2182 for PolyBench Java, and 2.2917 for SWE-EVO. Stratification exposes family differences; it does not eliminate domain confounding.

The historical report included financial-core/infrastructure subset figures with sample sizes 1,177 and 1,216. These sum to 2,393, not the full 2,925-issue corpus. The current script 06 computes keyword-based sets but does not output or validate that historical subset table. Those figures are therefore not retained as verified full-corpus sensitivity results in this edition.

Likewise, historical case coverage percentages (33.3% or 100%) are not retained as measured coverage results: the packaged artifacts do not provide a reproducible requirement-unit denominator and coverage calculation for those percentages. The source-based qualitative case comparisons remain available.

## 6. Codebook and traceability

The public [codebook snapshot](../data/framework-snapshot.json) retains its source criterion names and definitions. The package contains 3,446 task–criterion assignments in [ab_long.csv](../data/ab_long.csv) and 3,534 individual quotations in [ab_all_evidences.csv](../data/ab_all_evidences.csv). The historical count of 3,776 was inconsistent with these files and is corrected here.

The original report's boundary explanations are retained with the interface code corrected to B11:

| Criteria | Boundary explanation |
| :--- | :--- |
| B2 vs B3 | Arithmetic, amounts, and rate calculation concern B2; entity relationships and data consistency concern B3. |
| B4 vs A1 | A date-related business rule alone does not necessarily require temporal replay; use the source codebook to assess ordering and temporal semantics. |
| B6 vs B11 | Preserving existing stored data or effective behavior concerns B6; interface signatures and environment compatibility concern B11. B8 denotes authorization and protection. |
| B7 vs B9 | Transaction isolation, partial-failure control, and lock contention concern B7; resource use and leaks concern B9. |
| A2 vs A1 | Structural reorganization without a business-rule change is distinguished from product behavior. |
| A4 vs B7 | Operational scheduling is distinguished from transaction and concurrency guarantees. |

These explanations support review and do not redefine the frozen codebook. Evidence quotations and classification reasons make the assessments inspectable; deterministic export does not itself measure agreement between independent reviewers.

## 7. NodeBB #0030 source inspection

The task is from SWE-bench Pro v1. The base commit is `7800016f2f1b89d2d3cfea6a7da7c77096b7b927`.

- [Developer reference patch](../ablation_study/nodebb_0030/nodebb_0030_developer_patch.diff): 12 changed files; includes `src/upgrades/4.3.0/chat_allow_list.js`, with 44 added lines in a 50-line diff section.
- [Ablated patch](../ablation_study/nodebb_0030/nodebb_0030_ablated_patch.diff): 11 changed files, omitting that migration file. This is a constructed omission variant, not a recorded AI-generated solution.
- [Official test patch](../ablation_study/nodebb_0030/nodebb_0030_test_patch.diff): changes `test/messaging.js` and `test/user.js`.
- [Task specification](../ablation_study/nodebb_0030/nodebb_0030_spec.json), [inspection script](../ablation_study/nodebb_0030/inspect_nodebb_oracle.py), and [reproduction instructions](../ablation_study/nodebb_0030/README_ABLATION_REPRODUCTION.md).

The relevant added messaging tests create users, assign new allow-list settings directly, and assert `Messaging.canMessageUser` decisions. The inspected added test patch does not directly exercise the legacy-setting migration or its rerun behavior. This is a static specification-versus-assertion finding; no official benchmark score or container omission-pass result is reported here.

The NodeBB task remains in v2, but the explicit migration requirement was removed. The v1 finding does not transfer unchanged to v2. See [the review protocol and correction record](PAPER_GAP_AND_V2_REVIEW_PROTOCOL.md), [the structural review](V2_STRUCTURAL_REVIEW.md), and [the separate Proton follow-up experiment](V2_PIPELINE_OMISSION_CASE.md).

## 8. Packaged artifacts and reproduction

- [data/gate2_dependencies.csv](../data/gate2_dependencies.csv): 17 records, 17 columns: 16 core relationships and one technical reference.
- [data/gate2_case_mapping.csv](../data/gate2_case_mapping.csv): 4 records, 11 columns: case roles, anchors, and selection rationale.
- [data/gate2_harness_evidence.csv](../data/gate2_harness_evidence.csv): 4 records, 10 columns: assertion excerpts and scope.
- [data/gate2_case_verdicts.csv](../data/gate2_case_verdicts.csv): 4 records, 9 columns: conclusions and boundaries.
- [data/fineract/gate2_raw_source_snippets.json](../data/fineract/gate2_raw_source_snippets.json): Six issue descriptions and grounding records.
- [data/fineract/summary.json](../data/fineract/summary.json): Fineract criterion summary.
- [data/06_reviewer_rebuttal_metrics/fineract_issues.json](../data/06_reviewer_rebuttal_metrics/fineract_issues.json): 2,925 packaged issue records used by script 06.
- [data/e1_matched_pairs.csv](../data/e1_matched_pairs.csv): 1,177 pairs involving 581 distinct tasks; includes OpenLibrary 0143–0233.

Run from the package root after installing `requirements.txt`:

```bash
python scripts/05_generate_gate2_artifacts.py
python scripts/06_reviewer_rebuttal_metrics.py
python scripts/08_verify_gate2_master_plan.py
python ablation_study/nodebb_0030/inspect_nodebb_oracle.py
```

Script 05 overwrites the four Gate 2 CSVs with the encoded English records. Script 06 prints B-criterion distributions, selected co-occurrence/phi statistics, and benchmark-family profiles. It reads its issue input from `data/06_reviewer_rebuttal_metrics/`; it does not produce a domain-subset result table.

Script 08 checks codebook names and counts, all 20 quotation slices, corpus sizes, NodeBB patch structure, the E1 representative pair, and presence of the four E2 cases. Its case-list checks do not replace review of the case interpretations. The NodeBB inspection script performs static patch inspection.

## 9. Findings and interpretation

The source records document 16 business requirement relationships, distinguish explicit, co-required, and inferred relations, and retain one technical reference. The corpus statistics show differences in criterion co-occurrence, while the four benchmark cases illustrate different levels of assertion coverage.

The NodeBB v1 example shows a required migration path that is not directly asserted in the inspected added test patch. Element and RocketMQ demonstrate distinctions in abstraction and requirement scope; Navidrome supplies a positive stateful-testing example. These cases are not a prevalence estimate for all 944 tasks or a measurement of benchmark score inflation.

During this report update, script 06 completed successfully, script 08 passed its six checks with zero failures (including all 20 source-quotation slices), and the NodeBB static inspection script completed successfully. All three returned exit code 0. All relative links in this report were checked against the packaged files. The analysis CSV files and source code were not changed by this report update.
