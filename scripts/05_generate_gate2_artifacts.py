import os, csv

paper_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(paper_dir, "data")
os.makedirs(data_dir, exist_ok=True)

# ==============================================================================
# 1. gate2_dependencies.csv
# Grounding: Multi-Issue Requirement Dependency Structure from Fineract 2,925 Corpus
# Core Requirement Dependencies: 16 units (DEP-01 to DEP-16)
# Technical Call Path Reference: 1 supplementary unit (DEP-SUPP-01)
# ==============================================================================
dep_rows = [
    # -------------------------------------------------------------------------
    # Group 1: FINERACT-2338 (Resolved | Fixed, Historical Production Issue)
    # -------------------------------------------------------------------------
    {
        'dep_id': 'DEP-01',
        'issue_id': 'FINERACT-2338',
        'issue_status': 'Resolved',
        'issue_resolution': 'Fixed',
        'evidence_role': 'Historical Production Requirement (Resolved)',
        'from_code': 'A1',
        'from_name': 'Product Behavior and Business Rules (allow backdated interest-rate changes)',
        'to_code': 'B4',
        'to_name': 'Temporal and Sequential Semantics (trigger backdated reversal and replay)',
        'dependency_classification': 'Explicit Dependency',
        'quote_verification_status': 'Paired Verbatim Clauses',
        'verbatim_raw_quote': 'Backdate can be done on already paid Installments as well',
        'raw_quote_start_pos': 261,
        'paired_consequence_quote': 'Installments paid Interest amount will be reverse replayed as per the new Interest rate from the applied date',
        'paired_consequence_pos': 559,
        'causal_relationship_synthesis': 'The combination of allowing backdated changes to paid installments (Requirement Details #3) and the resulting cascading reversal and replay of interest amounts (Requirement Details #5) explicitly links the backdated change (A1) to reversal and replay (B4).',
        'boundary_and_invariance': 'Allow backdated interest rates to take effect from any past date after loan disbursement.'
    },
    {
        'dep_id': 'DEP-02',
        'issue_id': 'FINERACT-2338',
        'issue_status': 'Resolved',
        'issue_resolution': 'Fixed',
        'evidence_role': 'Historical Production Requirement (Resolved)',
        'from_code': 'B4',
        'from_name': 'Temporal and Sequential Semantics (backdated replay)',
        'to_code': 'B2',
        'to_name': 'Numerical and Computational Accuracy (recalculate repayment-schedule EMI and interest)',
        'dependency_classification': 'Explicit Dependency',
        'quote_verification_status': 'Exact Verbatim Match',
        'verbatim_raw_quote': 'Repayment schedule will be recalculated with New EMI and Interest from the Interest applied schedule date',
        'raw_quote_start_pos': 325,
        'paired_consequence_quote': 'N/A',
        'paired_consequence_pos': -1,
        'causal_relationship_synthesis': 'Backdated replay cascades into recalculating EMI and interest in the repayment schedule for paid, unpaid and partially paid installments from the effective date onward.',
        'boundary_and_invariance': 'Changes to principal/interest allocations in paid installments require cascading reversal and replay.'
    },
    {
        'dep_id': 'DEP-03',
        'issue_id': 'FINERACT-2338',
        'issue_status': 'Resolved',
        'issue_resolution': 'Fixed',
        'evidence_role': 'Historical Production Requirement (Resolved)',
        'from_code': 'B2',
        'from_name': 'Numerical and Computational Accuracy (recalculate EMI)',
        'to_code': 'B6',
        'to_name': 'Preservation of Existing Information and Behavior (invariant installment count)',
        'dependency_classification': 'Explicit Dependency',
        'quote_verification_status': 'Exact Verbatim Match',
        'verbatim_raw_quote': 'No of Installments will remain the same, only EMI and Interest would get affected',
        'raw_quote_start_pos': 843,
        'paired_consequence_quote': 'N/A',
        'paired_consequence_pos': -1,
        'causal_relationship_synthesis': "Although a backdated interest-rate change modifies each installment's EMI and interest amount, the total number of installments must remain unchanged.",
        'boundary_and_invariance': 'Structural invariant of the contractual ledger: preserve the total installment count.'
    },
    {
        'dep_id': 'DEP-04',
        'issue_id': 'FINERACT-2338',
        'issue_status': 'Resolved',
        'issue_resolution': 'Fixed',
        'evidence_role': 'Historical Production Requirement (Resolved)',
        'from_code': 'B4',
        'from_name': 'Temporal and Sequential Semantics (replay backdated transactions after charge-off)',
        'to_code': 'B3',
        'to_name': 'Data Relationships and Integrity (preserve standard accounting-entry rules)',
        'dependency_classification': 'Explicit Dependency',
        'quote_verification_status': 'Exact Verbatim Match',
        'verbatim_raw_quote': 'If the repayment that was made before the charge-off is reversed and replayed due to backdated Interest modification,then the accounting entry of the reversed transaction and replayed transaction should follow *standard accounting rules and not charge-off accounting rules*',
        'raw_quote_start_pos': 1005,
        'paired_consequence_quote': 'N/A',
        'paired_consequence_pos': -1,
        'causal_relationship_synthesis': 'When a repayment made before charge-off is reversed and replayed following a backdated interest change, the replayed entries must follow standard accounting rules rather than charge-off accounting rules.',
        'boundary_and_invariance': 'Control the invariant governing accounting-entry transitions for each ledger transaction state.'
    },

    # -------------------------------------------------------------------------
    # Group 2: FINERACT-753 (Resolved | Fixed, Historical Production Issue)
    # -------------------------------------------------------------------------
    {
        'dep_id': 'DEP-05',
        'issue_id': 'FINERACT-753',
        'issue_status': 'Resolved',
        'issue_resolution': 'Fixed',
        'evidence_role': 'Historical Production Requirement (Resolved)',
        'from_code': 'A1',
        'from_name': 'Product Behavior and Business Rules (cancel/reverse a savings deposit)',
        'to_code': 'B4, B2',
        'to_name': 'Temporal Replay and Balance Recalculation (trigger daily-balance recalculation)',
        'dependency_classification': 'Explicit Dependency',
        'quote_verification_status': 'Paired Verbatim Clauses',
        'verbatim_raw_quote': 'now reverse the deposit of 500 .',
        'raw_quote_start_pos': 1494,
        'paired_consequence_quote': 'system will\xa0recalculateDailyBalances and reverse the charge transaction on this section of the code',
        'paired_consequence_pos': 1532,
        'causal_relationship_synthesis': 'Reproduction Step 3 reverses a deposit of 500. The immediately following Step 4 states that the system calls recalculateDailyBalances, recalculates overdraft balances, and automatically reverses/reprocesses the associated charge transaction.',
        'boundary_and_invariance': 'Recalculate overdraft and daily balances from the cancellation date of the historical transaction.'
    },
    {
        'dep_id': 'DEP-06',
        'issue_id': 'FINERACT-753',
        'issue_status': 'Resolved',
        'issue_resolution': 'Fixed',
        'evidence_role': 'Historical Production Requirement (Resolved)',
        'from_code': 'B4',
        'from_name': 'Temporal and Sequential Semantics (create a replacement charge after reversal)',
        'to_code': 'B3, B6',
        'to_name': 'Data Relationships and Integrity (preserve charge-payment relationship objects)',
        'dependency_classification': 'Explicit Dependency',
        'quote_verification_status': 'Exact Verbatim Match',
        'verbatim_raw_quote': 'now since the new charge created does not have the charged paid by object in the table "\xa0 m_savings_account_charge_paid_by" recalculating the account balance becomes wrong',
        'raw_quote_start_pos': 2160,
        'paired_consequence_quote': 'N/A',
        'paired_consequence_pos': -1,
        'causal_relationship_synthesis': 'When a charge transaction is copied/recreated during daily-balance recalculation, omitting the m_savings_account_charge_paid_by relationship object corrupts subsequent balance recalculation.',
        'boundary_and_invariance': 'Missing foreign-key relationship objects corrupt account-ledger balances.'
    },

    # -------------------------------------------------------------------------
    # Group 3: FINERACT-2836 (In Progress | Unresolved, Active Enterprise Specification)
    # -------------------------------------------------------------------------
    {
        'dep_id': 'DEP-07',
        'issue_id': 'FINERACT-2836',
        'issue_status': 'In Progress',
        'issue_resolution': 'Unresolved',
        'evidence_role': 'Active Enterprise Maintenance Specification (Unresolved)',
        'from_code': 'B7',
        'from_name': 'Concurrency and Transaction Boundaries (independent transaction per installment)',
        'to_code': 'B6',
        'to_name': 'Preservation of Existing Information and Behavior (retain durable commits for successful installments)',
        'dependency_classification': 'Explicit Dependency',
        'quote_verification_status': 'Paired Verbatim Clauses',
        'verbatim_raw_quote': 'Each due savings-charge installment is processed in an independent transaction.',
        'raw_quote_start_pos': 853,
        'paired_consequence_quote': 'A successfully collected installment remains committed regardless of the outcome of another installment.',
        'paired_consequence_pos': 1016,
        'causal_relationship_synthesis': 'Each due savings-charge installment is processed in an independent transaction (AC #1), so successful ledger commits and balance deductions remain durable regardless of failures in other installments (AC #3).',
        'boundary_and_invariance': 'One due savings-charge installment defines the atomic transaction boundary.'
    },
    {
        'dep_id': 'DEP-08',
        'issue_id': 'FINERACT-2836',
        'issue_status': 'In Progress',
        'issue_resolution': 'Unresolved',
        'evidence_role': 'Active Enterprise Maintenance Specification (Unresolved)',
        'from_code': 'B7',
        'from_name': 'Transaction-Boundary Isolation',
        'to_code': 'B3',
        'to_name': 'Data Relationships and Integrity (prevent ledger-wide corruption after partial failure)',
        'dependency_classification': 'Inferred Dependency',
        'quote_verification_status': 'Inferred (Domain Engineering Principle)',
        'verbatim_raw_quote': 'Each due savings-charge installment is processed in an independent transaction.',
        'raw_quote_start_pos': 853,
        'paired_consequence_quote': 'N/A',
        'paired_consequence_pos': -1,
        'causal_relationship_synthesis': "The source explicitly requires independent transactions. Interpreting this as isolation intended to preserve relationships between other installments' ledger entries and account-balance entities after partial failure is a researcher interpretation based on software architecture principles.",
        'boundary_and_invariance': 'Distinguish the explicit independent-transaction requirement from the interpreted purpose of preserving data integrity.'
    },
    {
        'dep_id': 'DEP-09',
        'issue_id': 'FINERACT-2836',
        'issue_status': 'In Progress',
        'issue_resolution': 'Unresolved',
        'evidence_role': 'Active Enterprise Maintenance Specification (Unresolved)',
        'from_code': 'A4',
        'from_name': 'Execution and Operations (rerun a batch job)',
        'to_code': 'B6',
        'to_name': 'Preservation of Existing Information and Behavior (idempotency and prevention of duplicate collection)',
        'dependency_classification': 'Explicit Dependency',
        'quote_verification_status': 'Exact Verbatim Match',
        'verbatim_raw_quote': 'Re-running the job resumes from the first unpaid installment without collecting previously committed installments again.',
        'raw_quote_start_pos': 2293,
        'paired_consequence_quote': 'N/A',
        'paired_consequence_pos': -1,
        'causal_relationship_synthesis': 'The source explicitly requires a rerun batch job (A4) to skip already committed installments and resume at the first unpaid installment, directly enforcing idempotency and preventing duplicate collection (B6).',
        'boundary_and_invariance': 'Maintain transaction idempotency during batch-failure recovery.'
    },
    {
        'dep_id': 'DEP-10',
        'issue_id': 'FINERACT-2836',
        'issue_status': 'In Progress',
        'issue_resolution': 'Unresolved',
        'evidence_role': 'Active Enterprise Maintenance Specification (Unresolved)',
        'from_code': 'A1, B5',
        'from_name': 'Business Rules and State Workflow (handle insufficient balances)',
        'to_code': 'B7, B6',
        'to_name': 'Transaction Isolation and Preservation of Successful Batch Completion',
        'dependency_classification': 'Co-required',
        'quote_verification_status': 'Exact Verbatim Match',
        'verbatim_raw_quote': 'the job is not marked as failed solely because of the insufficient balance',
        'raw_quote_start_pos': 1718,
        'paired_consequence_quote': 'N/A',
        'paired_consequence_pos': -1,
        'causal_relationship_synthesis': 'An insufficient account balance is treated as a normal unpaid business outcome: the affected installment remains unpaid, but the entire batch job is not marked as failed.',
        'boundary_and_invariance': 'Isolate insufficient funds as an unpaid business state rather than a system exception.'
    },

    # -------------------------------------------------------------------------
    # Group 4: FINERACT-2930 (In Progress | Unresolved, Active Enterprise Specification)
    # -------------------------------------------------------------------------
    {
        'dep_id': 'DEP-11',
        'issue_id': 'FINERACT-2930',
        'issue_status': 'In Progress',
        'issue_resolution': 'Unresolved',
        'evidence_role': 'Active Enterprise Maintenance Specification (Unresolved)',
        'from_code': 'A1',
        'from_name': 'Product Behavior and Business Rules (correct a historical transaction)',
        'to_code': 'B4',
        'to_name': 'Temporal and Sequential Semantics (cascade replay from the earlier date)',
        'dependency_classification': 'Explicit Dependency',
        'quote_verification_status': 'Exact Verbatim Match',
        'verbatim_raw_quote': 'The loan is replayed from the earlier of the original and new transaction dates.',
        'raw_quote_start_pos': 2147,
        'paired_consequence_quote': 'N/A',
        'paired_consequence_pos': -1,
        'causal_relationship_synthesis': 'When a refund/waiver transaction date or amount is modified, replay the loan transaction sequence from the earlier of the original and new transaction dates.',
        'boundary_and_invariance': 'Require cascading invalidation through reversal of the original transaction and creation of a new transaction of the same type.'
    },
    {
        'dep_id': 'DEP-12',
        'issue_id': 'FINERACT-2930',
        'issue_status': 'In Progress',
        'issue_resolution': 'Unresolved',
        'evidence_role': 'Active Enterprise Maintenance Specification (Unresolved)',
        'from_code': 'B4',
        'from_name': 'Temporal and Sequential Semantics (backdated replay)',
        'to_code': 'B3, B2, B5',
        'to_name': 'Cascading Updates Across Entities (schedule, balances, allocations, accruals and status)',
        'dependency_classification': 'Co-required',
        'quote_verification_status': 'Exact Verbatim Match',
        'verbatim_raw_quote': 'The schedule, balances, allocations, accruals and loan status (e.g. closed \u2194 active, overpaid) are recalculated correctly.',
        'raw_quote_start_pos': 2228,
        'paired_consequence_quote': 'N/A',
        'paired_consequence_pos': -1,
        'causal_relationship_synthesis': 'Backdated replay cascades into recalculating the repayment schedule, ledger balances, payment allocations, accrued income and loan status together.',
        'boundary_and_invariance': 'A single transaction modification affects at least five core domain entities.'
    },
    {
        'dep_id': 'DEP-13',
        'issue_id': 'FINERACT-2930',
        'issue_status': 'In Progress',
        'issue_resolution': 'Unresolved',
        'evidence_role': 'Active Enterprise Maintenance Specification (Unresolved)',
        'from_code': 'A1',
        'from_name': 'Product Behavior and Business Rules (adjust a charge)',
        'to_code': 'B3',
        'to_name': 'Data Relationships and Integrity (preserve the original charge relationship)',
        'dependency_classification': 'Explicit Dependency',
        'quote_verification_status': 'Exact Verbatim Match',
        'verbatim_raw_quote': 'The new transaction stays linked to the same loan charge (LoanChargePaidBy / charge relation).',
        'raw_quote_start_pos': 3368,
        'paired_consequence_quote': 'N/A',
        'paired_consequence_pos': -1,
        'causal_relationship_synthesis': 'A new Charge Adjustment transaction must not be treated as an ordinary repayment; it must retain its relationship to the original charge entity through LoanChargePaidBy.',
        'boundary_and_invariance': 'Preserve one-to-one traceability between a charge and its adjustment transaction.'
    },
    {
        'dep_id': 'DEP-14',
        'issue_id': 'FINERACT-2930',
        'issue_status': 'In Progress',
        'issue_resolution': 'Unresolved',
        'evidence_role': 'Active Enterprise Maintenance Specification (Unresolved)',
        'from_code': 'A1, B3',
        'from_name': 'Business Rules and Relationships (restore a reversed transaction)',
        'to_code': 'B2',
        'to_name': 'Numerical and Computational Accuracy (recalculate the available adjustment limit)',
        'dependency_classification': 'Explicit Dependency',
        'quote_verification_status': 'Exact Verbatim Match',
        'verbatim_raw_quote': 'counting the reversed original as available again',
        'raw_quote_start_pos': 3561,
        'paired_consequence_quote': 'N/A',
        'paired_consequence_pos': -1,
        'causal_relationship_synthesis': 'A new adjustment amount must not exceed the available limit for the charge. Recalculate that limit by adding the reversed original transaction amount back to the available amount.',
        'boundary_and_invariance': 'Prevent excessive waivers by restoring the reversed transaction amount to the available adjustment limit.'
    },
    {
        'dep_id': 'DEP-15',
        'issue_id': 'FINERACT-2930',
        'issue_status': 'In Progress',
        'issue_resolution': 'Unresolved',
        'evidence_role': 'Domain Accounting Principle Interpretation',
        'from_code': 'B3, B2',
        'from_name': 'Relational Integrity and Numerical Accuracy',
        'to_code': 'B6',
        'to_name': 'Preservation of Existing Information and Behavior (ledger debit-credit invariant)',
        'dependency_classification': 'Inferred Dependency',
        'quote_verification_status': 'Inferred (Domain Accounting Principle)',
        'verbatim_raw_quote': 'Journal entries are reversed for the original transaction and posted for the new one, using the correct accounts for that transaction type.',
        'raw_quote_start_pos': 2357,
        'paired_consequence_quote': 'N/A',
        'paired_consequence_pos': -1,
        'causal_relationship_synthesis': 'After reversing a transaction and posting replacement journal entries, cumulative debits and credits in the loan-account ledger must remain consistent under double-entry accounting principles.',
        'boundary_and_invariance': 'The source explicitly requires journal posting; maintaining debit-credit balance is a researcher interpretation derived from financial-domain principles.'
    },

    # -------------------------------------------------------------------------
    # Group 5: FINERACT-2934 (Open | Unresolved, Active Enterprise Specification)
    # -------------------------------------------------------------------------
    {
        'dep_id': 'DEP-16',
        'issue_id': 'FINERACT-2934',
        'issue_status': 'Open',
        'issue_resolution': 'Unresolved',
        'evidence_role': 'Active Enterprise Maintenance Specification (Unresolved)',
        'from_code': 'A5',
        'from_name': 'Deployment, Versioning, and Environment Transition (consolidate configuration data through migration)',
        'to_code': 'B6',
        'to_name': 'Preservation of Existing Information and Behavior (preserve effective legacy behavior)',
        'dependency_classification': 'Explicit Dependency',
        'quote_verification_status': 'Exact Verbatim Match',
        'verbatim_raw_quote': 'For installations that already configured both rows, the effective behaviour does not change.',
        'raw_quote_start_pos': 1527,
        'paired_consequence_quote': 'N/A',
        'paired_consequence_pos': -1,
        'causal_relationship_synthesis': 'During a database migration that consolidates two settings (permission and limit) into one, copy the existing limit value and preserve the effective behavior of existing installations.',
        'boundary_and_invariance': "Preserve the existing system's effective runtime behavior after the Liquibase migration."
    },

    # -------------------------------------------------------------------------
    # Supplementary Group: Technical Call Trace Reference
    # -------------------------------------------------------------------------
    {
        'dep_id': 'DEP-SUPP-01',
        'issue_id': 'FINERACT-977',
        'issue_status': 'Resolved',
        'issue_resolution': 'Fixed',
        'evidence_role': 'Technical Runtime Call Trace (Supplementary Reference, not direct requirement specification)',
        'from_code': 'A2',
        'from_name': 'Technical Function Call Stack (internal schedule-generator calls)',
        'to_code': 'B1',
        'to_name': 'Internal Null-Pointer Defect Prevention (runtime exception handling)',
        'dependency_classification': 'Technical Call Graph',
        'quote_verification_status': 'Exact Verbatim Match',
        'verbatim_raw_quote': 'updateAmountsBasedOnCurrentEarlyPayments (AbstractLoanScheduleGenerator.java:640)',
        'raw_quote_start_pos': 239,
        'paired_consequence_quote': 'N/A',
        'paired_consequence_pos': -1,
        'causal_relationship_synthesis': 'The cascading stack trace between internal repayment-schedule generator methods during early-payment recalculation is supplementary technical evidence of a runtime call path, not a business requirement specification.',
        'boundary_and_invariance': 'Exclude this item from the 16 business requirement dependencies and retain it only as a technical reference.'
    }
]

dep_csv = os.path.join(data_dir, "gate2_dependencies.csv")
with open(dep_csv, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(dep_rows[0].keys()))
    writer.writeheader()
    writer.writerows(dep_rows)
print(f"Generated: {dep_csv} ({len(dep_rows)} rows: 16 core + 1 supplementary)")


# ==============================================================================
# 2. gate2_case_mapping.csv
# 4 Functional Comparative Axes: Mapping Industrial Need to Benchmark Scope
# Role Differentiation: Direct Comparison vs Evaluation Scope vs Concurrency Hierarchy vs Aligned Case
# ==============================================================================
map_rows = [
    {
        'axis_id': 'Axis-1',
        'comparative_role': 'Direct Functional Comparison',
        'functional_domain': 'Configuration Data Migration and Idempotency',
        'fineract_anchor': 'FINERACT-2934 (Open / Unresolved)',
        'fineract_dimension_and_codes': 'A5 (Deployment and Environment Transition), B6 (Preservation of Existing Data)',
        'fineract_core_requirement': 'A Liquibase migration that consolidates forced-withdrawal settings, copies existing limit values into the new structure in bulk, and preserves the effective behavior of existing installations.',
        'ai_task_id': '0030',
        'ai_repo': 'NodeBB/NodeBB',
        'ai_family': 'SWE-bench Pro',
        'ai_instance_id': 'instance_NodeBB__NodeBB-a5afad27e52fd336163063ba40dcadc80233ae10-vd59a5728dfc977f44533186ace531248c2917516',
        'selection_rationale': 'The problem statement explicitly requires a batch upgrade script (src/upgrades/4.3.0/chat_allow_list.js) to migrate accounts with restrictChat enabled to chatAllowList, including safe repeated execution. This provides a direct within-task comparison between configuration-migration requirements and evaluation-harness assertion scope.'
    },
    {
        'axis_id': 'Axis-2',
        'comparative_role': 'Evaluation Scope and Abstraction Gap',
        'functional_domain': 'Temporal State Transitions and Backdated Recalculation',
        'fineract_anchor': 'FINERACT-2930 (In Progress) / FINERACT-2338 (Resolved)',
        'fineract_dimension_and_codes': 'A1 (Transaction Modification) -> B4 (Backdated Replay) -> B2 (Numerical Calculation) -> B3 (Relational Integrity)',
        'fineract_core_requirement': 'After modifying a historical transaction date or amount, replay subsequent schedules, balances, journal entries and states from the earlier of the original and new dates.',
        'ai_task_id': '0139',
        'ai_repo': 'element-hq/element-web',
        'ai_family': 'SWE-bench Pro',
        'ai_instance_id': 'instance_element-hq__element-web-dae13ac8522fc6d41e64d1ac6e3174486fdcce0c-vnan',
        'selection_rationale': 'The task recalculates unread badges when read receipts are reordered across room and thread timelines. Its development purpose differs from backdated financial-ledger recalculation; it illustrates the localized in-memory state decisions measured by mock-based unit tests.'
    },
    {
        'axis_id': 'Axis-3',
        'comparative_role': 'Concurrency and Isolation-Level Hierarchy',
        'functional_domain': 'In-Process Thread Safety versus Business-Transaction Partial-Failure Isolation',
        'fineract_anchor': 'FINERACT-2836 (In Progress) / FINERACT-753 (Resolved)',
        'fineract_dimension_and_codes': 'B7 (Concurrency and Transaction Boundaries)',
        'fineract_core_requirement': 'Process each charge installment in an independent transaction to isolate partial failures, preserve successful commits when another installment has insufficient funds, and ensure idempotent reruns.',
        'ai_task_id': '0819',
        'ai_repo': 'apache/rocketmq',
        'ai_family': 'PolyBench Java',
        'ai_instance_id': 'apache__rocketmq-516',
        'selection_rationale': 'The task includes a high-load thread-safety stress test that makes StatsItemSet insertion atomic with putIfAbsent. It illustrates the distinction between atomic operations within one JVM and independent isolation and commit preservation in enterprise business transactions.'
    },
    {
        'axis_id': 'Axis-4',
        'comparative_role': 'Positive Benchmark Evaluation Case / Aligned Counterexample',
        'functional_domain': 'Database-Engine Backup, Schema Restoration and Retention Pruning',
        'fineract_anchor': 'Database Infrastructure Backup & Disaster Recovery Operational Baseline',
        'fineract_dimension_and_codes': 'A4 (Execution and Operations), B10 (Service Continuity and Failure Handling)',
        'fineract_core_requirement': 'Create backup files from a running database without service interruption and preserve schema-restoration integrity during recovery from destructive failures.',
        'ai_task_id': '0495',
        'ai_repo': 'navidrome/navidrome',
        'ai_family': 'SWE-bench Pro',
        'ai_instance_id': 'instance_navidrome__navidrome-55730514ea59d5f1d0b8e3f8745569c29bdbf7b4',
        'selection_rationale': 'The only task among the 944 analyzed tasks that tests persistent database operations using a running engine to create SQLite backups, restore after destructive DDL deletion, and enforce backup-count retention and pruning of old files.'
    }
]

map_csv = os.path.join(data_dir, "gate2_case_mapping.csv")
with open(map_csv, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(map_rows[0].keys()))
    writer.writeheader()
    writer.writerows(map_rows)
print(f"Generated: {map_csv} ({len(map_rows)} rows)")


# ==============================================================================
# 3. gate2_harness_evidence.csv
# Discrete Authentic Assertion Snippets (No Synthetic One-line Joining)
# ==============================================================================
harness_rows = [
    {
        'case_id': 'Case_NodeBB_0030',
        'task_id': '0030',
        'repo': 'NodeBB/NodeBB',
        'test_files': 'test/messaging.js, test/user.js',
        'engineering_correctness': "An appropriate unit permission test: directly asserts the allow/deny branches of canMessageUser() for mock users' settings and the exact [[error:chat-restricted]] error.",
        'actual_assertion_snippet': "await assert.rejects(Messaging.canMessageUser(uid2, uid1), { message: '[[error:chat-restricted]]' });",
        'evaluated_scope': 'Server-side leaf permission checks at chat-message submission time (in-memory permission gating).',
        'industrial_representativeness_gap': 'The F2P assertions do not include the legacy-account upgrade script (src/upgrades/4.3.0/chat_allow_list.js) or repeated-execution idempotency explicitly required by the specification, underrepresenting configuration-data migration within the inspected evaluation scope.',
        'unverified_industrial_conditions': 'Execution of the batch upgrade script; integrity of bulk database-key conversion for existing restrictChat=1 accounts; preservation of idempotency across repeated runs.',
        'boundary_calibration': "No execution experiment modified or removed the harness's complete regression tests. The evidence shows that the added F2P unit-test assertions focus on leaf permission branches."
    },
    {
        'case_id': 'Case_ElementWeb_0139',
        'task_id': '0139',
        'repo': 'element-hq/element-web',
        'test_files': 'test/Unread-test.ts, test/test-utils/threads.ts',
        'engineering_correctness': 'A thorough unit branch test: uses mocks to assert more than eight compound state-transition branches, including receipt reordering, self-sent messages and unread thread messages.',
        'actual_assertion_snippet': "expect(doesRoomHaveUnreadMessages(room)).toBe(true); expect(doesRoomHaveUnreadMessages(room)).toBe(false); [Mock: mocked(haveRendererForEvent).mockReturnValue(true); thread.initialEventsFetched = true;]",
        'evaluated_scope': 'Unread-badge decisions over synthesized room/thread event hierarchies held in memory (in-memory state-transition logic).',
        'industrial_representativeness_gap': 'The task does not require IndexedDB or live synchronization, so this is not a defect in the individual task. Passing these tests cannot be generalized to persistent-state consistency in a complex asynchronous distributed client.',
        'unverified_industrial_conditions': 'IndexedDB persistent-cache synchronization; stored-state updates when timeline events arrive out of order because of network latency; live synchronization-pipeline integration.',
        'boundary_calibration': 'Mocking is an appropriate unit-isolation technique. This case identifies the boundary of the measured capability rather than a defect in the individual evaluation.'
    },
    {
        'case_id': 'Case_RocketMQ_0819',
        'task_id': '0819',
        'repo': 'apache/rocketmq',
        'test_files': 'common/src/test/java/org/apache/rocketmq/common/stats/StatsItemSetTest.java',
        'engineering_correctness': 'A high-load concurrency stress test: submits 10,000 tasks through a ThreadPoolExecutor with 100 worker threads and repeats 50 times, asserting atomic putIfAbsent accumulation of 20,000L.',
        'actual_assertion_snippet': "assertEquals(20000L, test_unit().longValue()); [Framework: executor = new ThreadPoolExecutor(100, 200, 10, TimeUnit.SECONDS, new ArrayBlockingQueue<Runnable>(10000)); for (int i = 0; i < 50; i++) ...]",
        'evaluated_scope': 'Thread safety of shared-memory data structures within a single JVM (in-process multithreaded race conditions).',
        'industrial_representativeness_gap': 'The test provides strong verification of shared-memory atomicity within one JVM. Its evaluation level differs from independent business-transaction boundaries, partial-failure isolation, preservation of successful commits after failures, and duplicate-collection prevention on reruns as required by FINERACT-2836.',
        'unverified_industrial_conditions': 'Independent transaction boundaries per installment; durable commits for successful installments despite partial failures; idempotent reruns that prevent duplicate collection.',
        'boundary_calibration': 'A strong thread-safety test that illustrates the distinction between single-process memory concurrency and business-transaction isolation.'
    },
    {
        'case_id': 'Case_Navidrome_0495',
        'task_id': '0495',
        'repo': 'navidrome/navidrome',
        'test_files': 'db/backup_test.go',
        'engineering_correctness': 'An actual database-engine and file-management test: asserts SQLite backup creation, destructive DDL (DELETE FROM sqlite_master), backup restoration, and pruning of old files when the retention count is exceeded.',
        'actual_assertion_snippet': "Expect(isSchemaEmpty(Db().WriteDB())).To(BeFalse()); Expect(len(timesDecreasingChronologically) - pruneCount).To(Equal(expected)); Expect(err).To(MatchError(os.ErrNotExist)); [Setup: path, err := Db().Backup(ctx); ExecContext(ctx, 'DELETE FROM sqlite_master ...'); Expect(isSchemaEmpty(Db().WriteDB())).To(BeTrue());]",
        'evaluated_scope': 'SQLite backup-file creation, schema presence after destructive operations and restoration, and enforcement of backup-file retention pruning.',
        'industrial_representativeness_gap': 'A meaningful positive counterexample showing that a benchmark can test actual database-engine restoration and file-retention policies. The assertions remain at schema and file-existence levels and do not cover preservation of complex enterprise data relationships or business invariants.',
        'unverified_industrial_conditions': 'Preservation of individual business-table record values after restoration; complex foreign-key integrity; preservation of domain invariants.',
        'boundary_calibration': 'An aligned counterexample based on the test configuration and observed assertions, consistent with the Gate 1 labels (A4, B1, B4, B8, B10; B6 excluded).'
    }
]

harness_csv = os.path.join(data_dir, "gate2_harness_evidence.csv")
with open(harness_csv, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(harness_rows[0].keys()))
    writer.writeheader()
    writer.writerows(harness_rows)
print(f"Generated: {harness_csv} ({len(harness_rows)} rows)")


# ==============================================================================
# 4. gate2_case_verdicts.csv
# Academic Construct Underrepresentation Analysis: Beyond Binary Pass/Fail
# Calibrated Conclusions (Strictly Bounded to F2P Scope; No Conflation with Full Suite)
# ==============================================================================
verdict_rows = [
    {
        'case_id': 'Case_NodeBB_0030',
        'target_task': 'NodeBB Task #0030',
        'comparative_role': 'Direct Functional Comparison (configuration-data migration)',
        'engineering_soundness': 'Accurately verifies the intended unit permission logic (sound leaf permission test).',
        'evaluation_scope': 'Real-time messaging allow/deny decisions at the unit-function level (in-memory leaf logic).',
        'industrial_representativeness': 'The specification explicitly requires migration of existing settings and safe repeated execution (idempotency), but the inspected added F2P tests focus on messaging permission decisions.',
        'construct_underrepresentation_aspect': 'Underrepresents software evolution and persistent configuration migration, including idempotency.',
        'academic_conclusion': 'Although configuration migration and idempotency are explicit specification requirements, the added F2P unit-test assertions in test/messaging.js focus on leaf permission decisions and do not explicitly include migration execution or idempotency checks.',
        'certainty_and_boundary': 'A finding from static inspection of the added F2P assertions. The conclusion is restricted to their verification scope and does not assert a defect in the complete harness, including existing regression tests or P2P.'
    },
    {
        'case_id': 'Case_ElementWeb_0139',
        'target_task': 'Element-Web Task #0139',
        'comparative_role': 'Evaluation Scope and Abstraction Gap',
        'engineering_soundness': 'Precisely verifies complex receipt-related state-transition branches using mock objects (sound mock-based branch test).',
        'evaluation_scope': 'Unread-state decision branches over synthesized in-memory objects (in-memory state transitions).',
        'industrial_representativeness': 'Consistency of real client persistent storage (IndexedDB) and server synchronization pipelines is outside the evaluation scope.',
        'construct_underrepresentation_aspect': 'Underrepresents persistent client-state consistency and asynchronous synchronization invariants.',
        'academic_conclusion': 'Mocking is a legitimate unit-testing technique, but localized state-decision checks cannot be generalized to maintenance capability for a complex asynchronous distributed client; these are different levels of evaluated capability.',
        'certainty_and_boundary': 'Based on test-code and mock-object inspection. Mocking is described as a boundary of the measured capability, not as a defect.'
    },
    {
        'case_id': 'Case_RocketMQ_0819',
        'target_task': 'RocketMQ Task #0819',
        'comparative_role': 'Concurrency and Isolation-Level Hierarchy',
        'engineering_soundness': 'Directly verifies atomicity under high-load contention with 100 threads (sound multithreaded stress test).',
        'evaluation_scope': 'Thread safety of shared-memory data structures within a single process (in-process thread safety).',
        'industrial_representativeness': 'Shared-memory atomicity within one JVM is evaluated at a different level from independent isolation and commit preservation in enterprise business transactions.',
        'construct_underrepresentation_aspect': 'Underrepresents business-transaction partial-failure isolation and commit-preservation capability.',
        'academic_conclusion': 'This is a strong single-JVM concurrency test. Its success does not by itself establish independent business-transaction isolation, partial-failure isolation or commit-preservation capability; these are distinct development capabilities.',
        'certainty_and_boundary': 'Based on observed test parameters. The conclusion concerns business-transaction isolation and excludes two-phase commit or distributed-broker conditions not required by FINERACT-2836.'
    },
    {
        'case_id': 'Case_Navidrome_0495',
        'target_task': 'Navidrome Task #0495',
        'comparative_role': 'Positive Benchmark Evaluation Case / Aligned Counterexample',
        'engineering_soundness': 'Uses an actual SQLite engine to verify backup creation, restoration after destructive changes, and backup-file pruning (sound engine-level integration test).',
        'evaluation_scope': 'SQLite backup-file creation, schema-presence checks after destructive DDL (!isSchemaEmpty), and backup-retention count management.',
        'industrial_representativeness': 'Does not cover preservation of deeper enterprise business data or complex relational invariants.',
        'construct_underrepresentation_aspect': 'Partially represents persistent-data recovery, bounded to schema and retention rather than deeper business invariants.',
        'academic_conclusion': 'A strong positive counterexample demonstrating that benchmarks can test actual database-engine restoration and file-retention management, with verification depth restricted to schema and file levels.',
        'certainty_and_boundary': 'Based on the test configuration and observed assertions, consistent with the Gate 1 labels (A4, B1, B4, B8, B10; B6 excluded).'
    }
]

verdict_csv = os.path.join(data_dir, "gate2_case_verdicts.csv")
with open(verdict_csv, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(verdict_rows[0].keys()))
    writer.writeheader()
    writer.writerows(verdict_rows)
print(f"Generated: {verdict_csv} ({len(verdict_rows)} rows)")
