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
        'from_name': '제품 동작·업무 규칙 (소급 이자율 변경 허용)',
        'to_code': 'B4',
        'to_name': '시간·순서에 따른 의미 (소급 역분개 재처리 트리거)',
        'dependency_classification': 'Explicit Dependency',
        'quote_verification_status': 'Paired Verbatim Clauses',
        'verbatim_raw_quote': 'Backdate can be done on already paid Installments as well',
        'raw_quote_start_pos': 261,
        'paired_consequence_quote': 'Installments paid Interest amount will be reverse replayed as per the new Interest rate from the applied date',
        'paired_consequence_pos': 559,
        'causal_relationship_synthesis': '기납부 회차에 대한 소급 변경 허용(Requirement Details #3)과 이에 따른 이자 금액 연쇄 역분개 재처리(Requirement Details #5)의 결합을 통해, 소급 변경(A1)이 연쇄 역분개 재처리(B4)를 직접 트리거함을 명시함.',
        'boundary_and_invariance': '대출 실행일 이후 과거 모든 일자로부터 이자율 소급 적용 허용.'
    },
    {
        'dep_id': 'DEP-02',
        'issue_id': 'FINERACT-2338',
        'issue_status': 'Resolved',
        'issue_resolution': 'Fixed',
        'evidence_role': 'Historical Production Requirement (Resolved)',
        'from_code': 'B4',
        'from_name': '시간·순서에 따른 의미 (소급 재처리)',
        'to_code': 'B2',
        'to_name': '수치·계산 정확성 (상환 일정 EMI 및 이자 재계산)',
        'dependency_classification': 'Explicit Dependency',
        'quote_verification_status': 'Exact Verbatim Match',
        'verbatim_raw_quote': 'Repayment schedule will be recalculated with New EMI and Interest from the Interest applied schedule date',
        'raw_quote_start_pos': 325,
        'paired_consequence_quote': 'N/A',
        'paired_consequence_pos': -1,
        'causal_relationship_synthesis': '소급 재처리 실행 시 적용일 이후 기납부 및 미납/일부납 회차의 상환 일정에 대해 신규 EMI 및 이자를 연쇄적으로 재계산한다.',
        'boundary_and_invariance': '기납부 회차의 원금/이자 배분 변경 시 연쇄 역분개 재처리 강제.'
    },
    {
        'dep_id': 'DEP-03',
        'issue_id': 'FINERACT-2338',
        'issue_status': 'Resolved',
        'issue_resolution': 'Fixed',
        'evidence_role': 'Historical Production Requirement (Resolved)',
        'from_code': 'B2',
        'from_name': '수치·계산 정확성 (EMI 재산출)',
        'to_code': 'B6',
        'to_name': '기존 정보·동작 보존 (회차 총수 불변식)',
        'dependency_classification': 'Explicit Dependency',
        'quote_verification_status': 'Exact Verbatim Match',
        'verbatim_raw_quote': 'No of Installments will remain the same, only EMI and Interest would get affected',
        'raw_quote_start_pos': 843,
        'paired_consequence_quote': 'N/A',
        'paired_consequence_pos': -1,
        'causal_relationship_synthesis': '소급 이자율 변경으로 개별 회차의 EMI와 이자 금액이 변동되더라도, 전체 상환 회차 총수(No of Installments)는 변하지 않고 엄격히 보존되어야 한다.',
        'boundary_and_invariance': '계약 원장의 구조적 불변식: 회차 총수 불변.'
    },
    {
        'dep_id': 'DEP-04',
        'issue_id': 'FINERACT-2338',
        'issue_status': 'Resolved',
        'issue_resolution': 'Fixed',
        'evidence_role': 'Historical Production Requirement (Resolved)',
        'from_code': 'B4',
        'from_name': '시간·순서에 따른 의미 (상각 후 거래 소급 재처리)',
        'to_code': 'B3',
        'to_name': '데이터 관계·정합성 (표준 회계 분개 규칙 보존)',
        'dependency_classification': 'Explicit Dependency',
        'quote_verification_status': 'Exact Verbatim Match',
        'verbatim_raw_quote': 'If the repayment that was made before the charge-off is reversed and replayed due to backdated Interest modification,then the accounting entry of the reversed transaction and replayed transaction should follow *standard accounting rules and not charge-off accounting rules*',
        'raw_quote_start_pos': 1005,
        'paired_consequence_quote': 'N/A',
        'paired_consequence_pos': -1,
        'causal_relationship_synthesis': '대손 상각(charge-off) 이전에 납부된 거래가 소급 이자 변경으로 역분개 재처리될 때, 재처리 분개는 상각 회계 규칙이 아닌 표준 회계 분개 규칙을 유지해야 한다.',
        'boundary_and_invariance': '원장 거래 상태별 회계 분개 전이 불변식 통제.'
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
        'from_name': '제품 동작·업무 규칙 (예금 입금 취소/역분개)',
        'to_code': 'B4, B2',
        'to_name': '시간 재처리 및 잔액 재계산 (일일 잔액 재계산 트리거)',
        'dependency_classification': 'Explicit Dependency',
        'quote_verification_status': 'Paired Verbatim Clauses',
        'verbatim_raw_quote': 'now reverse the deposit of 500 .',
        'raw_quote_start_pos': 1494,
        'paired_consequence_quote': 'system will\xa0recalculateDailyBalances and reverse the charge transaction on this section of the code',
        'paired_consequence_pos': 1532,
        'causal_relationship_synthesis': '재현 절차 Step 3(입금 500 취소)이 실행되면 직후 Step 4에서 시스템이 recalculateDailyBalances를 호출하여 당좌대월 잔액을 재산출하고 연관 수수료 거래를 자동 취소/재처리함을 선후 절차로 명시함.',
        'boundary_and_invariance': '과거 거래 취소 시점부터 당좌대월 및 일일 잔액 전면 재계산.'
    },
    {
        'dep_id': 'DEP-06',
        'issue_id': 'FINERACT-753',
        'issue_status': 'Resolved',
        'issue_resolution': 'Fixed',
        'evidence_role': 'Historical Production Requirement (Resolved)',
        'from_code': 'B4',
        'from_name': '시간·순서에 따른 의미 (역분개 후 신규 수수료 생성)',
        'to_code': 'B3, B6',
        'to_name': '데이터 관계·정합성 (수수료 납부 관계 객체 보존)',
        'dependency_classification': 'Explicit Dependency',
        'quote_verification_status': 'Exact Verbatim Match',
        'verbatim_raw_quote': 'now since the new charge created does not have the charged paid by object in the table "\xa0 m_savings_account_charge_paid_by" recalculating the account balance becomes wrong',
        'raw_quote_start_pos': 2160,
        'paired_consequence_quote': 'N/A',
        'paired_consequence_pos': -1,
        'causal_relationship_synthesis': '일일 잔액 재계산 과정에서 수수료 거래가 복제/재생성될 때 m_savings_account_charge_paid_by 관계 객체가 누락되면 이후 잔액 재계산이 구조적으로 오염된다.',
        'boundary_and_invariance': '외래키 관계 객체 누락 시 계좌 잔액 원장 오염 발생.'
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
        'from_name': '동시 실행·트랜잭션 경계 (회차별 독립 트랜잭션)',
        'to_code': 'B6',
        'to_name': '기존 정보·동작 보존 (성공 회차 영속 커밋 보존)',
        'dependency_classification': 'Explicit Dependency',
        'quote_verification_status': 'Paired Verbatim Clauses',
        'verbatim_raw_quote': 'Each due savings-charge installment is processed in an independent transaction.',
        'raw_quote_start_pos': 853,
        'paired_consequence_quote': 'A successfully collected installment remains committed regardless of the outcome of another installment.',
        'paired_consequence_pos': 1016,
        'causal_relationship_synthesis': '각 회차별 저축 수수료는 독립 트랜잭션으로 처리되어(AC #1), 특정 회차의 실패 여부와 무관하게 성공 회차의 원장 커밋과 잔액 차감이 영속 보존된다(AC #3).',
        'boundary_and_invariance': '단일 회차(one due savings-charge installment)가 원자적 트랜잭션 경계임.'
    },
    {
        'dep_id': 'DEP-08',
        'issue_id': 'FINERACT-2836',
        'issue_status': 'In Progress',
        'issue_resolution': 'Unresolved',
        'evidence_role': 'Active Enterprise Maintenance Specification (Unresolved)',
        'from_code': 'B7',
        'from_name': '트랜잭션 경계 격리',
        'to_code': 'B3',
        'to_name': '데이터 관계·정합성 (부분 실패 시 전체 원장 오염 방지)',
        'dependency_classification': 'Inferred Dependency',
        'quote_verification_status': 'Inferred (Domain Engineering Principle)',
        'verbatim_raw_quote': 'Each due savings-charge installment is processed in an independent transaction.',
        'raw_quote_start_pos': 853,
        'paired_consequence_quote': 'N/A',
        'paired_consequence_pos': -1,
        'causal_relationship_synthesis': '원문은 독립 트랜잭션을 명시하며, 이것이 부분 실패 시 타 회차 원장 및 계좌 잔액 엔티티와의 관계 정합성을 보존하기 위한 격리 조치임은 소프트웨어 아키텍처 원리에 따른 연구자 해석임.',
        'boundary_and_invariance': '원문의 독립 트랜잭션 명시와 데이터 정합성 보존 목적의 해석을 분리 표기.'
    },
    {
        'dep_id': 'DEP-09',
        'issue_id': 'FINERACT-2836',
        'issue_status': 'In Progress',
        'issue_resolution': 'Unresolved',
        'evidence_role': 'Active Enterprise Maintenance Specification (Unresolved)',
        'from_code': 'A4',
        'from_name': '실행·운영 (배치 작업 재실행)',
        'to_code': 'B6',
        'to_name': '기존 정보·동작 보존 (멱등성 및 중복 징수 방지)',
        'dependency_classification': 'Explicit Dependency',
        'quote_verification_status': 'Exact Verbatim Match',
        'verbatim_raw_quote': 'Re-running the job resumes from the first unpaid installment without collecting previously committed installments again.',
        'raw_quote_start_pos': 2293,
        'paired_consequence_quote': 'N/A',
        'paired_consequence_pos': -1,
        'causal_relationship_synthesis': '배치 작업 재실행(A4) 시 이미 커밋된 이전 회차는 건너뛰고 첫 미납 회차부터 재개함으로써 멱등성과 중복 징수 방지(B6)를 직접 강제함을 원문이 명시함.',
        'boundary_and_invariance': '배치 장애 복구 시 트랜잭션 멱등성 보장.'
    },
    {
        'dep_id': 'DEP-10',
        'issue_id': 'FINERACT-2836',
        'issue_status': 'In Progress',
        'issue_resolution': 'Unresolved',
        'evidence_role': 'Active Enterprise Maintenance Specification (Unresolved)',
        'from_code': 'A1, B5',
        'from_name': '업무 규칙 및 상태 흐름 (잔액 부족 처리)',
        'to_code': 'B7, B6',
        'to_name': '트랜잭션 격리 및 배치 정상 완료 보존',
        'dependency_classification': 'Co-required',
        'quote_verification_status': 'Exact Verbatim Match',
        'verbatim_raw_quote': 'the job is not marked as failed solely because of the insufficient balance',
        'raw_quote_start_pos': 1718,
        'paired_consequence_quote': 'N/A',
        'paired_consequence_pos': -1,
        'causal_relationship_synthesis': '특정 계좌의 잔액 부족은 업무상 정상 미납 결과로 처리되어 해당 회차를 동결하되 전체 배치 작업을 실패 처리하지 않는다.',
        'boundary_and_invariance': '잔액 부족을 시스템 예외가 아닌 비즈니스 미납 상태로 격리.'
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
        'from_name': '제품 동작·업무 규칙 (과거 거래 정정)',
        'to_code': 'B4',
        'to_name': '시간·순서에 따른 의미 (이른 날짜 기준 연쇄 재처리)',
        'dependency_classification': 'Explicit Dependency',
        'quote_verification_status': 'Exact Verbatim Match',
        'verbatim_raw_quote': 'The loan is replayed from the earlier of the original and new transaction dates.',
        'raw_quote_start_pos': 2147,
        'paired_consequence_quote': 'N/A',
        'paired_consequence_pos': -1,
        'causal_relationship_synthesis': '환불/감면 거래의 일자나 금액 수정 시, 원 거래일과 신규 거래일 중 더 이른 날짜(earlier date)부터 대출 거래 전체를 연쇄 소급 재처리한다.',
        'boundary_and_invariance': '원 거래 취소 및 동일 타입 신규 거래 생성을 통한 연쇄 무효화 강제.'
    },
    {
        'dep_id': 'DEP-12',
        'issue_id': 'FINERACT-2930',
        'issue_status': 'In Progress',
        'issue_resolution': 'Unresolved',
        'evidence_role': 'Active Enterprise Maintenance Specification (Unresolved)',
        'from_code': 'B4',
        'from_name': '시간·순서에 따른 의미 (소급 재처리)',
        'to_code': 'B3, B2, B5',
        'to_name': '다중 엔티티 연쇄 갱신 (일정·잔액·배분·미수수익·상태)',
        'dependency_classification': 'Co-required',
        'quote_verification_status': 'Exact Verbatim Match',
        'verbatim_raw_quote': 'The schedule, balances, allocations, accruals and loan status (e.g. closed \u2194 active, overpaid) are recalculated correctly.',
        'raw_quote_start_pos': 2228,
        'paired_consequence_quote': 'N/A',
        'paired_consequence_pos': -1,
        'causal_relationship_synthesis': '소급 재처리 실행 결과로 상환 일정(schedule), 원장 잔액(balances), 상환 배분(allocations), 미수수익 발생액(accruals), 대출 상태(loan status)가 동시에 연쇄 재계산된다.',
        'boundary_and_invariance': '단일 거래 수정이 5개 이상의 핵심 도메인 엔티티에 파급.'
    },
    {
        'dep_id': 'DEP-13',
        'issue_id': 'FINERACT-2930',
        'issue_status': 'In Progress',
        'issue_resolution': 'Unresolved',
        'evidence_role': 'Active Enterprise Maintenance Specification (Unresolved)',
        'from_code': 'A1',
        'from_name': '제품 동작·업무 규칙 (수수료 조정 작업)',
        'to_code': 'B3',
        'to_name': '데이터 관계·정합성 (원 수수료 관계 링크 보존)',
        'dependency_classification': 'Explicit Dependency',
        'quote_verification_status': 'Exact Verbatim Match',
        'verbatim_raw_quote': 'The new transaction stays linked to the same loan charge (LoanChargePaidBy / charge relation).',
        'raw_quote_start_pos': 3368,
        'paired_consequence_quote': 'N/A',
        'paired_consequence_pos': -1,
        'causal_relationship_synthesis': '수수료 조정(Charge Adjustment) 신규 거래는 일반 상환 거래로 취급되지 않고 원 수수료 엔티티(LoanChargePaidBy)와의 연결 관계를 엄격히 유지해야 한다.',
        'boundary_and_invariance': '수수료-조정 거래 간 1:1 관계 추적성 보존.'
    },
    {
        'dep_id': 'DEP-14',
        'issue_id': 'FINERACT-2930',
        'issue_status': 'In Progress',
        'issue_resolution': 'Unresolved',
        'evidence_role': 'Active Enterprise Maintenance Specification (Unresolved)',
        'from_code': 'A1, B3',
        'from_name': '업무 규칙 및 관계 링크 (취소 거래 복원)',
        'to_code': 'B2',
        'to_name': '수치·계산 정확성 (가용 한도 재산출)',
        'dependency_classification': 'Explicit Dependency',
        'quote_verification_status': 'Exact Verbatim Match',
        'verbatim_raw_quote': 'counting the reversed original as available again',
        'raw_quote_start_pos': 3561,
        'paired_consequence_quote': 'N/A',
        'paired_consequence_pos': -1,
        'causal_relationship_synthesis': '신규 조정 금액은 해당 수수료의 가용 한도를 초과할 수 없으며, 취소된 원 거래의 금액을 가용 한도로 재산입하여 상한선을 재계산한다.',
        'boundary_and_invariance': '취소 거래 금액 가용 한도 복원을 통한 과다 감면 방지 통제.'
    },
    {
        'dep_id': 'DEP-15',
        'issue_id': 'FINERACT-2930',
        'issue_status': 'In Progress',
        'issue_resolution': 'Unresolved',
        'evidence_role': 'Domain Accounting Principle Interpretation',
        'from_code': 'B3, B2',
        'from_name': '관계 정합성 및 수치 정확성',
        'to_code': 'B6',
        'to_name': '기존 정보·동작 보존 (회계 원장 차대 불변식)',
        'dependency_classification': 'Inferred Dependency',
        'quote_verification_status': 'Inferred (Domain Accounting Principle)',
        'verbatim_raw_quote': 'Journal entries are reversed for the original transaction and posted for the new one, using the correct accounts for that transaction type.',
        'raw_quote_start_pos': 2357,
        'paired_consequence_quote': 'N/A',
        'paired_consequence_pos': -1,
        'causal_relationship_synthesis': '거래 취소 및 신규 분개 전표 전기 후, 대출 계좌의 누적 원장 차변과 대변의 합계는 복식부기 회계 원리에 따라 정합성을 유지해야 한다.',
        'boundary_and_invariance': '원문은 분개 전기를 명시하며, 차대 균형 유지는 금융 도메인 원리에 기초한 연구자 도출 해석임.'
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
        'from_name': '배포·버전·환경 전환 (설정 데이터 통합 마이그레이션)',
        'to_code': 'B6',
        'to_name': '기존 정보·동작 보존 (레거시 유효 동작 보존)',
        'dependency_classification': 'Explicit Dependency',
        'quote_verification_status': 'Exact Verbatim Match',
        'verbatim_raw_quote': 'For installations that already configured both rows, the effective behaviour does not change.',
        'raw_quote_start_pos': 1527,
        'paired_consequence_quote': 'N/A',
        'paired_consequence_pos': -1,
        'causal_relationship_synthesis': '이중 설정(허용 여부, 한도)을 단일 설정으로 통합하는 DB 마이그레이션 시, 기존 한도 설정값을 복제하고 기존 설치본의 유효 동작을 동일하게 보존한다.',
        'boundary_and_invariance': 'Liquibase 마이그레이션 실행 후 기존 시스템의 유효 런타임 행위 불변 보존.'
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
        'from_name': '기술적 함수 호출 스택 (스케줄러 생성기 내부 호출)',
        'to_code': 'B1',
        'to_name': '내부 널 포인터 결함 방어 (런타임 예외 방어)',
        'dependency_classification': 'Technical Call Graph',
        'quote_verification_status': 'Exact Verbatim Match',
        'verbatim_raw_quote': 'updateAmountsBasedOnCurrentEarlyPayments (AbstractLoanScheduleGenerator.java:640)',
        'raw_quote_start_pos': 239,
        'paired_consequence_quote': 'N/A',
        'paired_consequence_pos': -1,
        'causal_relationship_synthesis': '조기 상환 재계산 시 내부 상환 일정 생성기 메서드 간의 연쇄 호출 스택트레이스로서, 업무 요구사항이 아닌 런타임 함수 호출 경로를 증명하는 보조 기술 자료임.',
        'boundary_and_invariance': '업무 요구조건 의존관계 집계(16건)에서는 제외하고 기술 참조로만 활용.'
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
        'comparative_role': 'Direct Functional Comparison (직접 비교 사례)',
        'functional_domain': 'Configuration Data Migration & Idempotency (설정 데이터 이행 및 멱등성)',
        'fineract_anchor': 'FINERACT-2934 (Open / Unresolved)',
        'fineract_dimension_and_codes': 'A5 (배포·환경 전환), B6 (기존 데이터 보존)',
        'fineract_core_requirement': '강제 출금 설정 체계 단일화 시 기존 한도 값을 신규 구조로 일괄 복제 이행하고 기존 설치본의 유효 동작을 보존하는 Liquibase 마이그레이션',
        'ai_task_id': '0030',
        'ai_repo': 'NodeBB/NodeBB',
        'ai_family': 'SWE-bench Pro',
        'ai_instance_id': 'instance_NodeBB__NodeBB-a5afad27e52fd336163063ba40dcadc80233ae10-vd59a5728dfc977f44533186ace531248c2917516',
        'selection_rationale': '과제 문제 설명(Problem Statement)에서 기존 restrictChat 활성 계정을 chatAllowList로 이전하는 배치 업그레이드 스크립트(src/upgrades/4.3.0/chat_allow_list.js) 및 반복 실행 멱등성을 명시적으로 요구하여, 동일 과제 내부에서 설정 마이그레이션 요구조건과 평가 하네스 단언문의 범위를 1:1로 직접 비교할 수 있는 최적의 사례.'
    },
    {
        'axis_id': 'Axis-2',
        'comparative_role': 'Evaluation Scope & Abstraction Gap (평가 범위 및 추상화 층위의 차이를 설명하는 사례)',
        'functional_domain': 'Temporal State Transition & Recalculation (시간적 상태 전이 및 소급 재계산)',
        'fineract_anchor': 'FINERACT-2930 (In Progress) / FINERACT-2338 (Resolved)',
        'fineract_dimension_and_codes': 'A1 (거래 수정) -> B4 (소급 재처리) -> B2 (수치 계산) -> B3 (관계 정합성)',
        'fineract_core_requirement': '과거 거래 일자/금액 수정 시 원 거래일과 신규일 중 이른 날짜부터 후속 일정·잔액·분개·상태를 연쇄 소급 재처리',
        'ai_task_id': '0139',
        'ai_repo': 'element-hq/element-web',
        'ai_family': 'SWE-bench Pro',
        'ai_instance_id': 'instance_element-hq__element-web-dae13ac8522fc6d41e64d1ac6e3174486fdcce0c-vnan',
        'selection_rationale': '룸 타임라인과 스레드 타임라인 간에 읽음 영수증(receipt)이 역전될 때 미읽음 배지(badge) 소급 재계산을 다루지만, 금융의 소급 원장 재계산과는 개발 목적이 다르며, Mock 기반 단위 테스트가 측정하는 인메모리 상태 판정의 국소적 범위를 설명하는 사례.'
    },
    {
        'axis_id': 'Axis-3',
        'comparative_role': 'Concurrency & Isolation Level Hierarchy (동시성 및 격리 수준의 층위 차이를 설명하는 사례)',
        'functional_domain': 'In-Process Thread Safety vs Transaction Failure Isolation (단일 프로세스 스레드 안전성 vs 업무 트랜잭션 부분 실패 격리)',
        'fineract_anchor': 'FINERACT-2836 (In Progress) / FINERACT-753 (Resolved)',
        'fineract_dimension_and_codes': 'B7 (동시 실행·트랜잭션 경계)',
        'fineract_core_requirement': '수수료 부과 회차별 독립 트랜잭션 분리를 통한 부분 실패 격리, 잔액 부족 시 성공 건 커밋 보존 및 재실행 멱등성 보장',
        'ai_task_id': '0819',
        'ai_repo': 'apache/rocketmq',
        'ai_family': 'PolyBench Java',
        'ai_instance_id': 'apache__rocketmq-516',
        'selection_rationale': '다중 스레드 환경에서 StatsItemSet 테이블 삽입 시 발생하는 레이스 컨디션을 putIfAbsent로 원자화하는 고강도 스레드 안전성 스트레스 테스트를 포함하여, 단일 JVM 프로세스 내 원자적 연산과 엔터프라이즈 업무 트랜잭션의 독립 격리·커밋 보존 간의 층위 차이를 규명하는 사례.'
    },
    {
        'axis_id': 'Axis-4',
        'comparative_role': 'Positive Benchmark Evaluation Case / Aligned Counterexample (벤치마크의 긍정적 평가 사례 / 정합 반례)',
        'functional_domain': 'Engine Persistence Backup, Schema Restoration, and Retention Pruning (실제 DB 엔진 백업, 스키마 복원 및 보존 개수 정리)',
        'fineract_anchor': 'Database Infrastructure Backup & Disaster Recovery Operational Baseline',
        'fineract_dimension_and_codes': 'A4 (실행·운영), B10 (서비스 지속·실패 대응)',
        'fineract_core_requirement': '운영 중인 DB의 무중단 백업 파일 생성 및 파괴적 재해 복구 시 스키마 복원 무결성 보장',
        'ai_task_id': '0495',
        'ai_repo': 'navidrome/navidrome',
        'ai_family': 'SWE-bench Pro',
        'ai_instance_id': 'instance_navidrome__navidrome-55730514ea59d5f1d0b8e3f8745569c29bdbf7b4',
        'selection_rationale': 'SQLite 데이터베이스 백업 생성, 파괴적 DDL 삭제 후 복원, 그리고 백업 보존 개수 및 오래된 파일 정리(Pruning)를 실제 DB 엔진을 가동하여 검증하는 944개 과제 중 유일무이한 영속 DB 조작 테스트 과제.'
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
        'engineering_correctness': '적절한 단위 권한 테스트: mock 사용자의 allow/deny 설정에 따른 canMessageUser()의 차단/허용 분기 및 [[error:chat-restricted]] 에러 반환을 엄밀하게 단언함.',
        'actual_assertion_snippet': "await assert.rejects(Messaging.canMessageUser(uid2, uid1), { message: '[[error:chat-restricted]]' });",
        'evaluated_scope': '채팅 메시지 전송 시점의 서버 측 리프 권한 검사 (In-memory leaf permission gating)',
        'industrial_representativeness_gap': '문제 명세에서 명시적으로 요구한 레거시 계정의 업그레이드 마이그레이션 스크립트(src/upgrades/4.3.0/chat_allow_list.js) 및 반복 실행 멱등성 검증이 F2P 평가 단언문에 포함되지 않아, 설정 데이터 이행 역량이 평가 범위에서 축소 측정(Construct Underrepresentation)됨.',
        'unverified_industrial_conditions': '배치 업그레이드 스크립트의 실제 실행, 기존 restrictChat=1 사용자 계정의 DB 키 일괄 변환 정합성, 다중 실행 시 멱등성 보존.',
        'boundary_calibration': '하네스의 전체 회귀 테스트를 수정/삭제하여 실행 검증한 것이 아니며, F2P로 추가된 단위 테스트 단언문이 리프 권한 분기에 국한되어 있음을 실증함.'
    },
    {
        'case_id': 'Case_ElementWeb_0139',
        'task_id': '0139',
        'repo': 'element-hq/element-web',
        'test_files': 'test/Unread-test.ts, test/test-utils/threads.ts',
        'engineering_correctness': '우수한 단위 분기 테스트: 모의 객체(mock)를 활용하여 영수증 역전, 본인 전송, 스레드 미읽음 등 8개 이상의 복합 상태 전이 분기 로직을 충실하게 단언함.',
        'actual_assertion_snippet': "expect(doesRoomHaveUnreadMessages(room)).toBe(true); expect(doesRoomHaveUnreadMessages(room)).toBe(false); [Mock: mocked(haveRendererForEvent).mockReturnValue(true); thread.initialEventsFetched = true;]",
        'evaluated_scope': '메모리 상에서 합성된 룸/스레드 이벤트 계층에 대한 미읽음 배지 상태 판정 로직 (In-memory state transition logic)',
        'industrial_representativeness_gap': '원래 과제 범위가 IndexedDB나 라이브 동기화를 요구하지 않으므로 이는 개별 과제의 결함이 아님. 다만 이 테스트 통과를 복잡한 비동기 분산 클라이언트의 영속 상태 일관성 역량으로 일반화하여 해석할 수는 없음.',
        'unverified_industrial_conditions': 'IndexedDB 영속 캐시 동기화, 네트워크 지연에 따른 타임라인 이벤트 역순 도착 시 원장 갱신, 라이브 동기화 파이프라인 통합.',
        'boundary_calibration': '모킹 자체는 소프트웨어공학적으로 적절한 단위 격리 기법이며, 본 사례는 개별 평가 결함이 아니라 평가 대상 역량(Scope)의 경계를 규명함.'
    },
    {
        'case_id': 'Case_RocketMQ_0819',
        'task_id': '0819',
        'repo': 'apache/rocketmq',
        'test_files': 'common/src/test/java/org/apache/rocketmq/common/stats/StatsItemSetTest.java',
        'engineering_correctness': '고강도 동시성 스트레스 테스트: 100개 워커 스레드의 ThreadPoolExecutor로 10,000개 작업을 제출하고 50회 반복하여 putIfAbsent의 원자적 누적(20,000L)을 엄밀하게 단언함.',
        'actual_assertion_snippet': "assertEquals(20000L, test_unit().longValue()); [Framework: executor = new ThreadPoolExecutor(100, 200, 10, TimeUnit.SECONDS, new ArrayBlockingQueue<Runnable>(10000)); for (int i = 0; i < 50; i++) ...]",
        'evaluated_scope': '단일 JVM 프로세스 내부의 공유 메모리 자료구조 스레드 안전성 (In-process multi-threaded race condition)',
        'industrial_representativeness_gap': '단일 JVM 내 공유 메모리 원자적 연산 검증으로서는 매우 우수함. 그러나 이는 업무 트랜잭션 단위의 독립 트랜잭션 분리, 부분 실패 격리, 실패 시 성공 건 커밋 보존, 재실행 시 중복 징수 방지(FINERACT-2836 기준)와는 평가 대상의 층위가 다름.',
        'unverified_industrial_conditions': '회차별 독립 트랜잭션 경계 설정, 부분 실패 시 성공 건 영속 커밋, 재실행 시 중복 징수 방지 멱등성 보장.',
        'boundary_calibration': '스레드 안전성 검증으로서 매우 훌륭한 테스트이며, 본 사례는 단일 프로세스 메모리 동시성과 업무 트랜잭션 격리 간의 층위 차이를 보여줌.'
    },
    {
        'case_id': 'Case_Navidrome_0495',
        'task_id': '0495',
        'repo': 'navidrome/navidrome',
        'test_files': 'db/backup_test.go',
        'engineering_correctness': '실제 DB 엔진 조작 및 파일 관리 테스트: 실제 SQLite 백업 파일 생성, 파괴적 DDL 실행(DELETE FROM sqlite_master), 백업 복원 동작, 그리고 백업 보존 개수 초과 시 오래된 백업 파일 정리(Pruning)를 오류 없이 엄밀하게 단언함.',
        'actual_assertion_snippet': "Expect(isSchemaEmpty(Db().WriteDB())).To(BeFalse()); Expect(len(timesDecreasingChronologically) - pruneCount).To(Equal(expected)); Expect(err).To(MatchError(os.ErrNotExist)); [Setup: path, err := Db().Backup(ctx); ExecContext(ctx, 'DELETE FROM sqlite_master ...'); Expect(isSchemaEmpty(Db().WriteDB())).To(BeTrue());]",
        'evaluated_scope': 'SQLite 백업 파일 생성, 파괴 후 복원 시 스키마 존재 여부, 및 백업 파일 보존 정책(Retention Pruning) 실행 검증',
        'industrial_representativeness_gap': '벤치마크가 실제 DB 엔진 복원과 파일 보존 정책을 테스트할 수 있음을 입증하는 유의미한 긍정 반례임. 다만 단언문의 깊이가 스키마 레벨과 파일 존재성에 머물러 복합 엔터프라이즈 데이터 관계 및 업무 불변식 보존까지는 포괄하지 않음.',
        'unverified_industrial_conditions': '복원 후 개별 비즈니스 테이블 레코드의 값 보존, 복합 외래키 관계 무결성, 도메인 불변식 보존.',
        'boundary_calibration': '테스트 구성 및 단언문 실측에 기반하며, Gate 1 분류(A4, B1, B4, B8, B10; B6 미포함)와의 정합성을 엄격히 유지하는 정합 반례임.'
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
        'comparative_role': 'Direct Functional Comparison (설정 데이터 이행 직접 비교)',
        'engineering_soundness': '의도된 단위 권한 판정 로직을 정확히 검증함 (Sound Leaf Permission Test)',
        'evaluation_scope': '단위 함수 레벨의 실시간 메시징 허용/거부 판정 (In-memory leaf logic)',
        'industrial_representativeness': '과제 명세에는 기존 설정의 마이그레이션과 반복 실행 안전성(idempotency)이 명시되어 있지만, 분석된 F2P 추가 테스트는 메시징 권한 판정에 집중되어 있음',
        'construct_underrepresentation_aspect': '소프트웨어 진화 및 영속 설정 이행 역량의 축소 측정 (Underrepresents Configuration Migration & Idempotency)',
        'academic_conclusion': '과제 명세에는 설정 마이그레이션과 멱등성이 명시되어 있으나, 추가된 F2P 단위 테스트 단언문(test/messaging.js)은 리프 권한 판정에 집중되어 있어, F2P 평가 단언문에 설정 마이그레이션 실행 및 멱등성 검사가 명시적으로 포함되지 않음을 입증함.',
        'certainty_and_boundary': 'F2P 추가 테스트 단언문 정적 분석에 기반한 명확한 사실이며, 기존 회귀 테스트나 P2P를 포함한 전체 하네스의 결함을 주장하는 것이 아니라 F2P 추가 평가 단언문의 검증 범위로 결론을 엄격히 한정함.'
    },
    {
        'case_id': 'Case_ElementWeb_0139',
        'target_task': 'Element-Web Task #0139',
        'comparative_role': 'Evaluation Scope & Abstraction Gap (평가 범위 및 추상화 층위 차이 설명)',
        'engineering_soundness': '모의 객체를 통해 복잡한 영수증 분기 상태 전이를 정밀하게 검증함 (Sound Mock-based Branch Test)',
        'evaluation_scope': '인메모리 합성 객체 상에서의 미읽음 상태 판정 분기 로직 (In-memory state transitions)',
        'industrial_representativeness': '실제 클라이언트 영속 스토리지(IndexedDB) 및 서버 동기화 파이프라인 정합성은 평가 범위 밖임',
        'construct_underrepresentation_aspect': '영속 클라이언트 상태 일관성 및 비동기 동기화 역량의 축소 측정 (Underrepresents Persistent State & Sync Invariants)',
        'academic_conclusion': '모킹 자체는 정당한 단위 테스트 기법이나, 국소 상태 판단 검증만으로 복잡한 비동기 분산 클라이언트의 유지보수 역량을 평가했다고 일반화할 수는 없음 (평가 능력 층위의 차이).',
        'certainty_and_boundary': '테스트 코드 및 모의 객체 분석에 기반하며, 모킹을 결함으로 보지 않고 측정 대상 역량의 경계로 정확히 기술함.'
    },
    {
        'case_id': 'Case_RocketMQ_0819',
        'target_task': 'RocketMQ Task #0819',
        'comparative_role': 'Concurrency & Isolation Level Hierarchy (동시성 층위 차이 설명)',
        'engineering_soundness': '100개 스레드 고부하 경합 환경에서 원자성을 엄밀하게 검증함 (Sound Multi-thread Stress Test)',
        'evaluation_scope': '단일 프로세스 공유 메모리 자료구조의 스레드 안전성 (In-process thread-safety)',
        'industrial_representativeness': '단일 JVM 공유 메모리 원자성과 엔터프라이즈 업무 트랜잭션의 독립 격리·커밋 보존 요구와는 평가 층위가 다름',
        'construct_underrepresentation_aspect': '업무 트랜잭션 부분 실패 격리 및 커밋 보존 역량의 축소 측정 (Underrepresents Business Transaction Failure Isolation)',
        'academic_conclusion': '단일 JVM 동시성 검증으로서는 매우 훌륭한 테스트이나, 이 성공이 곧 업무 트랜잭션 단위의 독립 격리, 부분 실패 격리, 커밋 보존 역량을 의미하지는 않음 (서로 다른 개발 역량의 공존).',
        'certainty_and_boundary': '테스트 파라미터 실측에 기반하며, FINERACT-2836에 없는 2PC나 분산 브로커 조건을 배제하고 업무 트랜잭션 격리 층위 차이로 엄격히 한정함.'
    },
    {
        'case_id': 'Case_Navidrome_0495',
        'target_task': 'Navidrome Task #0495',
        'comparative_role': 'Positive Benchmark Evaluation Case / Aligned Counterexample (긍정 평가 반례)',
        'engineering_soundness': '실제 SQLite DB 엔진을 가동하여 백업 생성, 파괴 후 복원, 및 백업 파일 정리(Pruning)를 성공적으로 검증함 (Sound Engine-level Integration Test)',
        'evaluation_scope': 'SQLite 백업 파일 생성, 파괴적 DDL 후 스키마 존재 여부 확인 (!isSchemaEmpty), 및 백업 보존 개수 관리',
        'industrial_representativeness': '엔터프라이즈의 심층 비즈니스 데이터 및 복합 관계 불변식 보존까지는 포괄하지 못함',
        'construct_underrepresentation_aspect': '영속 데이터 심층 비즈니스 불변식 역량의 부분적 대표 (Partially Represents DB Recovery, Bounded to Schema & Retention)',
        'academic_conclusion': '벤치마크가 실제 DB 엔진 복원과 파일 보존 관리를 테스트할 수 있음을 입증하는 강력한 긍정 반례이지만, 검증의 깊이는 스키마 및 파일 레벨로 한정됨 (정합 반례를 통한 평가 지평의 객관적 제시).',
        'certainty_and_boundary': '테스트 구성 및 단언문 실측에 기반하며, Gate 1 분류(A4, B1, B4, B8, B10; B6 미포함)와의 정합성을 엄격히 유지함.'
    }
]

verdict_csv = os.path.join(data_dir, "gate2_case_verdicts.csv")
with open(verdict_csv, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(verdict_rows[0].keys()))
    writer.writeheader()
    writer.writerows(verdict_rows)
print(f"Generated: {verdict_csv} ({len(verdict_rows)} rows)")
