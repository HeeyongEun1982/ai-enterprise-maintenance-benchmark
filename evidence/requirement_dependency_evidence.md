# Requirement Dependency Evidence and Benchmark Family Profiles

Study: **Beyond Surface Metrics: Multi-Condition Requirements in Enterprise Maintenance and AI Coding Benchmarks**.

This document assembles the Gate 3 statistical tables and source-grounded relationship evidence from the current public package. It covers 2,925 Fineract issues (3,811 requirement units) and 944 benchmark tasks: SWE-bench Pro v1 (731), PolyBench Java (165), and SWE-EVO (48).

Paths in code spans are relative to the `git/` package root. All links resolve within the package. The [source codebook](../data/framework-snapshot.json) is unchanged; English criterion descriptions below are display translations.

## 1. Three analytical levels

### Level 1: Per-task multi-attribute diversity

The number of distinct B1–B12 conditions assigned to an issue or task is its B-criterion count, denoted |B|. It describes the breadth of co-present fulfillment conditions. It does not measure directional dependency depth, and B criteria are not restricted to nonfunctional qualities.

### Level 2: Corpus-level statistical co-occurrence

Phi describes association between two binary criterion indicators across a corpus. A coefficient near zero describes weak observed association; a nonsignificant test does not establish exact independence. Co-occurrence does not determine causal direction or explain how benchmark tasks were selected.

### Level 3: Source-grounded directional relationships

Source clauses identify sequences, triggers, consequences, and preservation obligations. The [dependency records](../data/gate2_dependencies.csv) distinguish 12 explicit dependencies, two co-required relationships, and two inferred dependencies. Co-required listings do not by themselves establish direction, and inferred relationships retain their interpretive status. A separate technical reference is excluded from the 16 core business relationships.

## 2. Benchmark-family distributions

### Table 1. Criterion frequencies across three benchmark families

These values come from [the stratified metrics CSV](../data/gate3_stratified_family_metrics.csv). A task can have several criteria; percentages therefore do not sum to 100%.

| Code | Criterion (English description) | AI pooled (944) | SWE-bench Pro (731) | PolyBench Java (165) | SWE-EVO (48) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| A1 | Product behavior and business rules | 426 (45.13%) | 300 (41.04%) | 84 (50.91%) | 42 (87.50%) |
| A2 | Structure and implementation approach | 572 (60.59%) | 505 (69.08%) | 50 (30.30%) | 17 (35.42%) |
| A3 | Testing and quality assurance | 94 (9.96%) | 70 (9.58%) | 10 (6.06%) | 14 (29.17%) |
| A4 | Execution and operations | 122 (12.92%) | 93 (12.72%) | 20 (12.12%) | 9 (18.75%) |
| A5 | Deployment, version, and environment transitions | 60 (6.36%) | 39 (5.34%) | 9 (5.45%) | 12 (25.00%) |
| A6 | Development process, documentation, and project support | 53 (5.61%) | 25 (3.42%) | 17 (10.30%) | 11 (22.92%) |
| B1 | Functional results and input conditions | 315 (33.37%) | 276 (37.76%) | 25 (15.15%) | 14 (29.17%) |
| B2 | Numerical and calculation accuracy | 65 (6.89%) | 49 (6.70%) | 11 (6.67%) | 5 (10.42%) |
| B3 | Data relationships and consistency | 214 (22.67%) | 184 (25.17%) | 25 (15.15%) | 5 (10.42%) |
| B4 | Temporal and ordering semantics | 86 (9.11%) | 77 (10.53%) | 7 (4.24%) | 2 (4.17%) |
| B5 | State and business workflows | 131 (13.88%) | 109 (14.91%) | 20 (12.12%) | 2 (4.17%) |
| B6 | Preservation of existing information and behavior | 368 (38.98%) | 336 (45.96%) | 17 (10.30%) | 15 (31.25%) |
| B7 | Concurrent execution and transaction boundaries | 42 (4.45%) | 35 (4.79%) | 4 (2.42%) | 3 (6.25%) |
| B8 | Authorization and protection | 154 (16.31%) | 130 (17.78%) | 16 (9.70%) | 8 (16.67%) |
| B9 | Performance and resource use | 83 (8.79%) | 60 (8.21%) | 13 (7.88%) | 10 (20.83%) |
| B10 | Service continuity and failure handling | 87 (9.22%) | 72 (9.85%) | 8 (4.85%) | 7 (14.58%) |
| B11 | Interface and environment compatibility | 391 (41.42%) | 311 (42.54%) | 51 (30.91%) | 29 (60.42%) |
| B12 | User interaction | 183 (19.39%) | 169 (23.12%) | 4 (2.42%) | 10 (20.83%) |

### Table 2. B-criterion count distributions

The [distribution CSV](../data/gate3_coupling_complexity.csv) stores all nine bins (0–8). This table shows all bins rather than combining the upper tail. Means and medians are calculated from the frequency distributions.

| Measure | Fineract (2,925) | AI pooled (944) | Pro (731) | PolyBench (165) | EVO (48) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Mean | 1.7798 | 2.2447 | 2.4733 | 1.2182 | 2.2917 |
| Median | 2.0 | 2.0 | 2.0 | 1.0 | 2.0 |
| &#124;B&#124; = 0 | 331 (11.32%) | 3 (0.32%) | 0 (0.00%) | 3 (1.82%) | 0 (0.00%) |
| &#124;B&#124; = 1 | 872 (29.81%) | 248 (26.27%) | 109 (14.91%) | 126 (76.36%) | 13 (27.08%) |
| &#124;B&#124; = 2 | 1,097 (37.50%) | 357 (37.82%) | 304 (41.59%) | 33 (20.00%) | 20 (41.67%) |
| &#124;B&#124; = 3 | 451 (15.42%) | 231 (24.47%) | 219 (29.96%) | 3 (1.82%) | 9 (18.75%) |
| &#124;B&#124; = 4 | 112 (3.83%) | 79 (8.37%) | 77 (10.53%) | 0 (0.00%) | 2 (4.17%) |
| &#124;B&#124; = 5 | 37 (1.26%) | 15 (1.59%) | 12 (1.64%) | 0 (0.00%) | 3 (6.25%) |
| &#124;B&#124; = 6 | 21 (0.72%) | 6 (0.64%) | 6 (0.82%) | 0 (0.00%) | 0 (0.00%) |
| &#124;B&#124; = 7 | 4 (0.14%) | 3 (0.32%) | 2 (0.27%) | 0 (0.00%) | 1 (2.08%) |
| &#124;B&#124; = 8 | 0 (0.00%) | 2 (0.21%) | 2 (0.27%) | 0 (0.00%) | 0 (0.00%) |

SWE-bench Pro has a mean B-criterion count of 2.4733 versus 1.7798 for Fineract. The Welch comparison computed by the verifier gives t = 15.78 and p = 4.29e-51. Pro has at least two B criteria in 85.09% of tasks; 76.36% of PolyBench Java tasks have one B criterion. Counts alone do not establish whether a task is a local function fix, how difficult it is, or how deeply its tests inspect a dependency path.

## 3. Corpus-level criterion-pair associations

### Table 3. Co-occurrence counts, phi, and Fisher exact p-values

The [correlation CSV](../data/gate3_phi_correlation_matrix.csv) contains 11 selected pairs. P-values below test association within each corpus; they are not tests of the difference between the two phi coefficients and are not adjusted for multiple comparisons.

| Pair | Fineract co-occurrence | Fineract phi | Fineract p | AI co-occurrence | AI phi | AI p |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| B4-B2 | 254 | +0.430 | 2.76e-95 | 5 | -0.013 | 0.825 |
| A1-B4 | 471 | +0.309 | 1.71e-72 | 42 | +0.024 | 0.496 |
| A1-B2 | 440 | +0.343 | 3.2e-98 | 34 | +0.039 | 0.246 |
| A1-B3 | 538 | +0.329 | 1.56e-80 | 115 | +0.094 | 0.00486 |
| B4-B3 | 138 | +0.069 | 0.000252 | 22 | +0.022 | 0.501 |
| B4-B6 | 84 | +0.068 | 0.000457 | 28 | -0.042 | 0.246 |
| B2-B3 | 189 | +0.226 | 5.62e-30 | 14 | -0.007 | 1 |
| B2-B6 | 64 | +0.036 | 0.0545 | 19 | -0.054 | 0.113 |
| B3-B6 | 89 | +0.053 | 0.00503 | 63 | -0.106 | 0.00108 |
| B7-B6 | 8 | +0.005 | 0.696 | 14 | -0.025 | 0.519 |
| B7-B3 | 20 | +0.040 | 0.0407 | 7 | -0.031 | 0.451 |

B4–B2 co-occurs in 254 Fineract issues (phi +0.430) and five AI tasks (phi -0.013, p approximately 0.825). The five tasks are 0.53% of all AI tasks. The observed corpus contrast does not establish an absence of all such combinations or a causal explanation of the difference. Directional source relationships are examined separately below.

## 4. Fineract source-grounded relationships

### Table 4. Core relationships and supplementary technical reference

This table reproduces the [dependency CSV](../data/gate2_dependencies.csv), including exact quotations and character offsets into [the packaged Jira descriptions](../data/fineract/gate2_raw_source_snippets.json). The 16 core records have 19 quotations including paired consequences. The supplementary record brings the total to 20. Open and in-progress issues supply requirement evidence, not proof of completed implementation.

| ID | Issue (status) | Classification | Recorded relation | Source quote | Paired consequence | Synthesis and boundary |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| DEP-01 | FINERACT-2338 (Resolved) | Explicit Dependency | A1 -> B4 | Backdate can be done on already paid Installments as well (pos: 261, len: 57) | Installments paid Interest amount will be reverse replayed as per the new Interest rate from the applied date (pos: 559, len: 109) | The combination of allowing backdated changes to paid installments (Requirement Details #3) and the resulting cascading reversal and replay of interest amounts (Requirement Details #5) explicitly links the backdated change (A1) to reversal and replay (B4). Allow backdated interest rates to take effect from any past date after loan disbursement. |
| DEP-02 | FINERACT-2338 (Resolved) | Explicit Dependency | B4 -> B2 | Repayment schedule will be recalculated with New EMI and Interest from the Interest applied schedule date (pos: 325, len: 105) | N/A | Backdated replay cascades into recalculating EMI and interest in the repayment schedule for paid, unpaid and partially paid installments from the effective date onward. Changes to principal/interest allocations in paid installments require cascading reversal and replay. |
| DEP-03 | FINERACT-2338 (Resolved) | Explicit Dependency | B2 -> B6 | No of Installments will remain the same, only EMI and Interest would get affected (pos: 843, len: 81) | N/A | Although a backdated interest-rate change modifies each installment's EMI and interest amount, the total number of installments must remain unchanged. Structural invariant of the contractual ledger: preserve the total installment count. |
| DEP-04 | FINERACT-2338 (Resolved) | Explicit Dependency | B4 -> B3 | If the repayment that was made before the charge-off is reversed and replayed due to backdated Interest modification,then the accounting entry of the reversed transaction and replayed transaction should follow *standard accounting rules and not charge-off accounting rules* (pos: 1005, len: 273) | N/A | When a repayment made before charge-off is reversed and replayed following a backdated interest change, the replayed entries must follow standard accounting rules rather than charge-off accounting rules. Control the invariant governing accounting-entry transitions for each ledger transaction state. |
| DEP-05 | FINERACT-753 (Resolved) | Explicit Dependency | A1 -> B4, B2 | now reverse the deposit of 500 . (pos: 1494, len: 32) | system will recalculateDailyBalances and reverse the charge transaction on this section of the code (pos: 1532, len: 99) | Reproduction Step 3 reverses a deposit of 500. The immediately following Step 4 states that the system calls recalculateDailyBalances, recalculates overdraft balances, and automatically reverses/reprocesses the associated charge transaction. Recalculate overdraft and daily balances from the cancellation date of the historical transaction. |
| DEP-06 | FINERACT-753 (Resolved) | Explicit Dependency | B4 -> B3, B6 | now since the new charge created does not have the charged paid by object in the table "  m_savings_account_charge_paid_by" recalculating the account balance becomes wrong (pos: 2160, len: 171) | N/A | When a charge transaction is copied/recreated during daily-balance recalculation, omitting the m_savings_account_charge_paid_by relationship object corrupts subsequent balance recalculation. Missing foreign-key relationship objects corrupt account-ledger balances. |
| DEP-07 | FINERACT-2836 (In Progress) | Explicit Dependency | B7 -> B6 | Each due savings-charge installment is processed in an independent transaction. (pos: 853, len: 79) | A successfully collected installment remains committed regardless of the outcome of another installment. (pos: 1016, len: 104) | Each due savings-charge installment is processed in an independent transaction (AC #1), so successful ledger commits and balance deductions remain durable regardless of failures in other installments (AC #3). One due savings-charge installment defines the atomic transaction boundary. |
| DEP-08 | FINERACT-2836 (In Progress) | Inferred Dependency | B7 -> B3 | Each due savings-charge installment is processed in an independent transaction. (pos: 853, len: 79) | N/A | The source explicitly requires independent transactions. Interpreting this as isolation intended to preserve relationships between other installments' ledger entries and account-balance entities after partial failure is a researcher interpretation based on software architecture principles. Distinguish the explicit independent-transaction requirement from the interpreted purpose of preserving data integrity. |
| DEP-09 | FINERACT-2836 (In Progress) | Explicit Dependency | A4 -> B6 | Re-running the job resumes from the first unpaid installment without collecting previously committed installments again. (pos: 2293, len: 120) | N/A | The source explicitly requires a rerun batch job (A4) to skip already committed installments and resume at the first unpaid installment, directly enforcing idempotency and preventing duplicate collection (B6). Maintain transaction idempotency during batch-failure recovery. |
| DEP-10 | FINERACT-2836 (In Progress) | Co-required | A1, B5 -> B7, B6 | the job is not marked as failed solely because of the insufficient balance (pos: 1718, len: 74) | N/A | An insufficient account balance is treated as a normal unpaid business outcome: the affected installment remains unpaid, but the entire batch job is not marked as failed. Isolate insufficient funds as an unpaid business state rather than a system exception. |
| DEP-11 | FINERACT-2930 (In Progress) | Explicit Dependency | A1 -> B4 | The loan is replayed from the earlier of the original and new transaction dates. (pos: 2147, len: 80) | N/A | When a refund/waiver transaction date or amount is modified, replay the loan transaction sequence from the earlier of the original and new transaction dates. Require cascading invalidation through reversal of the original transaction and creation of a new transaction of the same type. |
| DEP-12 | FINERACT-2930 (In Progress) | Co-required | B4 -> B3, B2, B5 | The schedule, balances, allocations, accruals and loan status (e.g. closed ↔ active, overpaid) are recalculated correctly. (pos: 2228, len: 122) | N/A | Backdated replay cascades into recalculating the repayment schedule, ledger balances, payment allocations, accrued income and loan status together. A single transaction modification affects at least five core domain entities. |
| DEP-13 | FINERACT-2930 (In Progress) | Explicit Dependency | A1 -> B3 | The new transaction stays linked to the same loan charge (LoanChargePaidBy / charge relation). (pos: 3368, len: 94) | N/A | A new Charge Adjustment transaction must not be treated as an ordinary repayment; it must retain its relationship to the original charge entity through LoanChargePaidBy. Preserve one-to-one traceability between a charge and its adjustment transaction. |
| DEP-14 | FINERACT-2930 (In Progress) | Explicit Dependency | A1, B3 -> B2 | counting the reversed original as available again (pos: 3561, len: 49) | N/A | A new adjustment amount must not exceed the available limit for the charge. Recalculate that limit by adding the reversed original transaction amount back to the available amount. Prevent excessive waivers by restoring the reversed transaction amount to the available adjustment limit. |
| DEP-15 | FINERACT-2930 (In Progress) | Inferred Dependency | B3, B2 -> B6 | Journal entries are reversed for the original transaction and posted for the new one, using the correct accounts for that transaction type. (pos: 2357, len: 139) | N/A | After reversing a transaction and posting replacement journal entries, cumulative debits and credits in the loan-account ledger must remain consistent under double-entry accounting principles. The source explicitly requires journal posting; maintaining debit-credit balance is a researcher interpretation derived from financial-domain principles. |
| DEP-16 | FINERACT-2934 (Open) | Explicit Dependency | A5 -> B6 | For installations that already configured both rows, the effective behaviour does not change. (pos: 1527, len: 93) | N/A | During a database migration that consolidates two settings (permission and limit) into one, copy the existing limit value and preserve the effective behavior of existing installations. Preserve the existing system's effective runtime behavior after the Liquibase migration. |
| DEP-SUPP-01 | FINERACT-977 (Resolved) | Technical Call Graph | A2 -> B1 | updateAmountsBasedOnCurrentEarlyPayments (AbstractLoanScheduleGenerator.java:640) (pos: 239, len: 81) | N/A | The cascading stack trace between internal repayment-schedule generator methods during early-payment recalculation is supplementary technical evidence of a runtime call path, not a business requirement specification. Exclude this item from the 16 business requirement dependencies and retain it only as a technical reference. |

The relation codes preserve the CSV's notation. Classification distinguishes explicit links from co-required conditions and inferred interpretations; arrows in a record do not erase that distinction.

## 5. Benchmark cases and test-assertion scope

### Table 5. Four illustrative cases

The [case mapping](../data/gate2_case_mapping.csv), [harness evidence](../data/gate2_harness_evidence.csv), and [case verdicts](../data/gate2_case_verdicts.csv) provide the underlying records. This table summarizes qualitative scope; it does not assign a numerical coverage percentage without an operational requirement-unit denominator.

| Axis and task | Role | Specification anchor | Test files and assertions | Scope and conclusion |
| :--- | :--- | :--- | :--- | :--- |
| Axis-1 / NodeBB/NodeBB #0030 | Direct Functional Comparison | The problem statement explicitly requires a batch upgrade script (src/upgrades/4.3.0/chat_allow_list.js) to migrate accounts with restrictChat enabled to chatAllowList, including safe repeated execution. This provides a direct within-task comparison between configuration-migration requirements and evaluation-harness assertion scope. | test/messaging.js, test/user.js: await assert.rejects(Messaging.canMessageUser(uid2, uid1), { message: '[[error:chat-restricted]]' }); | Although configuration migration and idempotency are explicit specification requirements, the added F2P unit-test assertions in test/messaging.js focus on leaf permission decisions and do not explicitly include migration execution or idempotency checks. A finding from static inspection of the added F2P assertions. The conclusion is restricted to their verification scope and does not assert a defect in the complete harness, including existing regression tests or P2P. |
| Axis-2 / element-hq/element-web #0139 | Evaluation Scope and Abstraction Gap | The task recalculates unread badges when read receipts are reordered across room and thread timelines. Its development purpose differs from backdated financial-ledger recalculation; it illustrates the localized in-memory state decisions measured by mock-based unit tests. | test/Unread-test.ts, test/test-utils/threads.ts: expect(doesRoomHaveUnreadMessages(room)).toBe(true); expect(doesRoomHaveUnreadMessages(room)).toBe(false); [Mock: mocked(haveRendererForEvent).mockReturnValue(true); thread.initialEventsFetched = true;] | Mocking is a legitimate unit-testing technique, but localized state-decision checks cannot be generalized to maintenance capability for a complex asynchronous distributed client; these are different levels of evaluated capability. Based on test-code and mock-object inspection. Mocking is described as a boundary of the measured capability, not as a defect. |
| Axis-3 / apache/rocketmq #0819 | Concurrency and Isolation-Level Hierarchy | The task includes a high-load thread-safety stress test that makes StatsItemSet insertion atomic with putIfAbsent. It illustrates the distinction between atomic operations within one JVM and independent isolation and commit preservation in enterprise business transactions. | common/src/test/java/org/apache/rocketmq/common/stats/StatsItemSetTest.java: assertEquals(20000L, test_unit().longValue()); [Framework: executor = new ThreadPoolExecutor(100, 200, 10, TimeUnit.SECONDS, new ArrayBlockingQueue<Runnable>(10000)); for (int i = 0; i < 50; i++) ...] | This is a strong single-JVM concurrency test. Its success does not by itself establish independent business-transaction isolation, partial-failure isolation or commit-preservation capability; these are distinct development capabilities. Based on observed test parameters. The conclusion concerns business-transaction isolation and excludes two-phase commit or distributed-broker conditions not required by FINERACT-2836. |
| Axis-4 / navidrome/navidrome #0495 | Positive Benchmark Evaluation Case / Aligned Counterexample | The only task among the 944 analyzed tasks that tests persistent database operations using a running engine to create SQLite backups, restore after destructive DDL deletion, and enforce backup-count retention and pruning of old files. | db/backup_test.go: Expect(isSchemaEmpty(Db().WriteDB())).To(BeFalse()); Expect(len(timesDecreasingChronologically) - pruneCount).To(Equal(expected)); Expect(err).To(MatchError(os.ErrNotExist)); [Setup: path, err := Db().Backup(ctx); ExecContext(ctx, 'DELETE FROM sqlite_master ...'); Expect(isSchemaEmpty(Db().WriteDB())).To(BeTrue());] | A strong positive counterexample demonstrating that benchmarks can test actual database-engine restoration and file-retention management, with verification depth restricted to schema and file levels. Based on the test configuration and observed assertions, consistent with the Gate 1 labels (A4, B1, B4, B8, B10; B6 excluded). |

- **NodeBB #0030:** the v1 specification requires migration of legacy settings and safe repeated execution. The reference patch includes 44 migration lines in a 50-line diff section; the constructed variant omits that file. Added tests set new lists directly and assert permission decisions. This is static inspection of the added patch, not an official execution-pass result.
- **Element-Web #0139:** mocked unread-state decisions illustrate test abstraction. Inferred IndexedDB persistence obligations are not treated as omitted explicit requirements.
- **RocketMQ #0819:** the threaded test addresses single-JVM atomicity. Fineract's business-transaction isolation and preservation requirements describe a different scope.
- **Navidrome #0495:** SQLite backup/restoration and file-pruning assertions provide a positive stateful-testing example.

NodeBB sources and the inspection script are in [the NodeBB reproduction folder](../ablation_study/nodebb_0030/README_ABLATION_REPRODUCTION.md). The other original task records are in [data/ai_case_sources/](../data/ai_case_sources/). The [v2 review protocol](PAPER_GAP_AND_V2_REVIEW_PROTOCOL.md) and [Proton follow-up experiment](V2_PIPELINE_OMISSION_CASE.md) document later version-specific work separately.

## 6. Regeneration and verification

Run from the `git/` package root after installing `requirements.txt`:

```bash
python scripts/09_generate_gate3_artifacts.py
python scripts/09_verify_gate3.py
```

The generator overwrites the three Gate 3 CSVs. This evidence document is maintained separately. The verifier recomputes distributions, correlations, and means; checks source quotation slices; inspects selected benchmark patch strings; and checks this document's level headings, Fineract mean, dependency IDs, offsets, and configured wording.

These checks do not parse every table cell in this document. During this update, Tables 1–5 were assembled directly from the packaged CSV records, and all local links were checked. Original analysis CSVs and the source codebook were preserved. Manuscript placement instructions have been removed from this public evidence document.

After the English document and its search strings were updated, `09_verify_gate3.py` passed all six checks with zero failures and exit code 0, including 19 core source-quotation slices and the three English analytical-level headings.
