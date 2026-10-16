# [Gate 3 실증 보고서] 엔터프라이즈 유지보수 요구사항 인과 의존관계 및 3대 AI 벤치마크 패밀리 층화 증거 문서
## Enterprise Maintenance Requirement Dependency Chains & 3-Family Stratified Benchmark Evidence
### Document Reference: `requirement_dependency_evidence.md` (v0.4 Master Plan Edition)

* **논문 제목**: *Beyond Task Complexity: Mapping Enterprise Maintenance Requirements to AI Coding Benchmark Evaluation*
* **목표 학술대회**: **BenchSOC 2026** (CEUR-ART 1-Column Format, 최대 12페이지)
* **작업 단계**: **Gate 3 — 정량 통계 정밀화 및 인과 사슬 1:1 증거표 작성**
* **연계 데이터셋**:
  - Apache Fineract 유지보수 코퍼스 ($N=2,925$, 3,811개 요구 단위)
  - AI 코딩 벤치마크 기준 과제 ($N=944$: SWE-bench Pro 731건, PolyBench Java 165건, SWE-EVO 48건)
  - 공식 18개 기준 코드북 ([`framework-snapshot.json`](../data/framework-snapshot.json))

---

## 1. 방법론적 기초: 속성 다양성, 통계적 공기, 인과 사슬의 3단계 엄밀한 구분

본 연구는 요구조건 분석에서 발생하기 쉬운 개념적 혼선을 방지하기 위해 다음 세 가지 분석 층위를 학술적으로 명확히 분리하여 규명합니다:

1. **층위 1: 과제별 다중 속성 출현 다양성 (Attribute Diversity, $|B|$)**:
   - 단일 과제 이슈 설명 내에 동시에 태깅된 B 조건(B1~B12)의 개수(비순서 집합의 크기 $|\{B_i\}| = k$)입니다.
   - 이는 한 과제가 담고 있는 비기능적/품질 속성의 외형적 '다양성' 또는 '동시 출현 폭'을 나타내며, 조건 간의 방향성 있는 인과 사슬이나 의존관계 깊이(Dependency Depth)를 의미하지 않습니다.
2. **층위 2: 코퍼스 수준의 통계적 공기 상관성 (Statistical Co-occurrence via $\phi$)**:
   - 피어슨-파이 상관계수($\phi$)는 대규모 코퍼스(Fineract 2,925건 vs AI 벤치마크 944건) 전체에서 특정 두 요구조건이 과제 단위로 함께 등장하는 선형적 상관 경향을 나타냅니다.
   - $\phi \approx 0$은 분석 대상 표본 집단 내에서 두 조건의 선형 공기 연관성이 관측되지 않음을 뜻하는 경험적 관찰값이며, 수학적 의미의 완전한 독립성을 증명하는 것은 아닙니다.
3. **층위 3: 미시적 방향성 인과 의존관계 (Directed Causal Dependency via Verbatim Quotes & Tests)**:
   - 두 조건 간의 구체적인 선후 관계, 트리거-결과절, 그리고 불변식 제약(Trigger $\rightarrow$ Consequence $\models$ Invariance)은 통계치만으로 유추하지 않고, 원문 대조가 완료된 **16개 핵심 업무 의존관계의 원문 쌍 연결 인용구**([`gate2_dependencies.csv`](../data/gate2_dependencies.csv))와 실제 코드·테스트 오라클 단언문 분석을 통해 직접 입증합니다.

---

## 2. 3대 AI 벤치마크 패밀리 계층별 실제 층화 통계 (Benchmark Family Stratified Profile)

AI 코딩 벤치마크 944개 전체를 단일 집단으로 뭉뚱그리지 않고, 원본 메타데이터에 기반하여 **3대 벤치마크 패밀리(SWE-bench Pro 731건, PolyBench Java 165건, SWE-EVO 48건)**로 층화 분석한 실측 통계는 다음과 같습니다 ([`gate3_stratified_family_metrics.csv`](../data/gate3_stratified_family_metrics.csv)).

### [Table 1] 공식 18개 기준별 AI 벤치마크 3대 패밀리 층화 출현 빈도 및 비율 ($N=944$)

| 코드 | 기준 공식 명칭 (Immutable Codebook) | AI 전체 (N=944)<br>건수 / 비율(%) | SWE-bench Pro (N=731)<br>건수 / 비율(%) | PolyBench Java (N=165)<br>건수 / 비율(%) | SWE-EVO (N=48)<br>건수 / 비율(%) |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **A1** | **제품 동작·업무 규칙** | 426건 (45.13%) | 300건 (41.04%) | 84건 (50.91%) | 42건 (87.50%) |
| **A2** | **구조·구현 방식** | 572건 (60.59%) | 505건 (69.08%) | 50건 (30.30%) | 17건 (35.42%) |
| **A3** | **시험·품질 확인** | 94건 ( 9.96%) | 70건 ( 9.58%) | 10건 ( 6.06%) | 14건 (29.17%) |
| **A4** | **실행·운영** | 122건 (12.92%) | 93건 (12.72%) | 20건 (12.12%) | 9건 (18.75%) |
| **A5** | **배포·버전·환경 전환** | 60건 ( 6.36%) | 39건 ( 5.34%) | 9건 ( 5.45%) | 12건 (25.00%) |
| **A6** | **개발 절차·문서·프로젝트 지원** | 53건 ( 5.61%) | 25건 ( 3.42%) | 17건 (10.30%) | 11건 (22.92%) |
| **B1** | **기능 결과·입력 조건** | 315건 (33.37%) | 276건 (37.76%) | 25건 (15.15%) | 14건 (29.17%) |
| **B2** | **수치·계산 정확성** | 65건 ( 6.89%) | 49건 ( 6.70%) | 11건 ( 6.67%) | 5건 (10.42%) |
| **B3** | **데이터 관계·정합성** | 214건 (22.67%) | 184건 (25.17%) | 25건 (15.15%) | 5건 (10.42%) |
| **B4** | **시간·순서에 따른 의미** | 86건 ( 9.11%) | 77건 (10.53%) | 7건 ( 4.24%) | 2건 ( 4.17%) |
| **B5** | **상태·업무 흐름** | 131건 (13.88%) | 109건 (14.91%) | 20건 (12.12%) | 2건 ( 4.17%) |
| **B6** | **기존 정보·동작의 보존** | 368건 (38.98%) | 336건 (45.96%) | 17건 (10.30%) | 15건 (31.25%) |
| **B7** | **동시 실행·트랜잭션 경계** | 42건 ( 4.45%) | 35건 ( 4.79%) | 4건 ( 2.42%) | 3건 ( 6.25%) |
| **B8** | **권한·보호** | 154건 (16.31%) | 130건 (17.78%) | 16건 ( 9.70%) | 8건 (16.67%) |
| **B9** | **성능·자원 사용** | 83건 ( 8.79%) | 60건 ( 8.21%) | 13건 ( 7.88%) | 10건 (20.83%) |
| **B10**| **서비스 지속·실패 대응** | 87건 ( 9.22%) | 72건 ( 9.85%) | 8건 ( 4.85%) | 7건 (14.58%) |
| **B11**| **인터페이스·환경 호환** | 391건 (41.42%) | 311건 (42.54%) | 51건 (30.91%) | 29건 (60.42%) |
| **B12**| **사용자 상호작용** | 183건 (19.39%) | 169건 (23.12%) | 4건 ( 2.42%) | 10건 (20.83%) |

* **실측 무결성 확인**: 과거 v0.3에서 발생했던 0% 파싱 오류는 전면 해소되었으며, 18개 기준 전 항목이 3개 패밀리 전체에서 실제 관측치로 계산됨.

---

### [Table 2] 다중 속성 출현 다양성 ($|B|$) 계열별 분포 비교 (Multi-Attribute Co-presence)

개별 과제 하나가 포함하는 속성(B1~B12)의 동시 출현 개수($|B|$) 분포는 벤치마크 패밀리 간에 뚜렷한 차이를 보입니다 ([`gate3_coupling_complexity.csv`](../data/gate3_coupling_complexity.csv)):

| 다양성 지표 | Fineract (N=2,925) | AI 전체 (N=944) | SWE-bench Pro (N=731) | PolyBench Java (N=165) | SWE-EVO (N=48) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **평균 출현 개수 (Mean $|B|$)** | **1.78개** (1.7798) | **2.24개** (2.2447) | **2.47개** (2.4733) | **1.22개** (1.2182) | **2.29개** (2.2917) |
| **중앙값 (Median $|B|$)** | **2.0개** | **2.0개** | **2.0개** | **1.0개** | **2.0개** |
| **$|B| = 0$ (속성 없음)** | 331건 (11.32%) | 3건 ( 0.32%) | 0건 ( 0.00%) | 3건 ( 1.82%) | 0건 ( 0.00%) |
| **$|B| = 1$ (단일 속성)** | 872건 (29.81%) | 248건 (26.27%) | 109건 (14.91%) | **126건 (76.36%)** | 13건 (27.08%) |
| **$|B| = 2$ (2개 속성)** | 1,097건 (37.50%) | 357건 (37.82%) | 304건 (41.59%) | 33건 (20.00%) | 20건 (41.67%) |
| **$|B| = 3$ (3개 속성)** | 451건 (15.42%) | 231건 (24.47%) | 219건 (29.96%) | 3건 ( 1.82%) | 9건 (18.75%) |
| **$|B| \ge 4$ (4개 이상 다중 속성)** | 174건 ( 5.95%) | 105건 (11.12%) | 99건 (13.54%) | 0건 ( 0.00%) | 6건 (12.50%) |

* **패밀리 간 핵심 관찰 및 학술적 해석**:
  - **SWE-bench Pro의 속성 다양성 인정**: SWE-bench Pro의 평균 B 조건 출현 개수는 **2.47개**로 Fineract의 **1.78개**보다 수치상 더 높게 나타납니다 (두 독립 표본 간 평균 차이 검정: Welch's $t = 15.78, p < 10^{-50}$, 평균 차이 $+0.69$, 95% CI $[+0.61, +0.78]$). 2개 이상의 속성이 함께 나타나는 비율($|B| \ge 2$) 역시 85.09%에 달합니다. 이는 AI 벤치마크가 모든 면에서 단순하다는 이분법적 가설을 기각하며, Pro 계열이 회귀 방지($B_6$), 인터페이스 호환($B_{11}$), 권한($B_8$) 등 다양한 비기능/품질 속성을 폭넓게 포괄하고 있음을 실증합니다.
  - **PolyBench Java의 국소성**: PolyBench Java는 단일 속성 과제($|B|=1$)가 **76.36%**에 달하여, 국소 단위 함수 수준의 입출력 버그 수정 중심이라는 특성을 뚜렷하게 보여줍니다.
  - **속성 수와 인과 구조의 분리**: 따라서 본 연구의 진정한 기여는 "AI 벤치마크에 속성이 몇 개나 태깅되어 있는가"라는 단순 개수 비교에 있지 않습니다. 평균 2.47개의 속성이 출현하는 SWE-bench Pro에서도, 조건들 간의 실질적인 공기 상관 양상(Table 3)과 인과적 의존 구조(Table 4, 5)는 엔터프라이즈 환경과 질적으로 다른 양상을 보입니다.

---

## 3. 핵심 의존 사슬 공기 빈도 및 파이 상관계수 행렬 ($\phi$ Correlation Matrix)

대규모 코퍼스(Fineract 2,925건 vs AI 벤치마크 944건) 전체에서 주요 기준 쌍의 공기 빈도와 피어슨-파이($\phi$) 상관계수를 전수 산출한 결과는 다음과 같습니다 ([`gate3_phi_correlation_matrix.csv`](../data/gate3_phi_correlation_matrix.csv)):

### [Table 3] 주요 요구조건 쌍별 공기 빈도 및 $\phi$ 상관계수 비교

| 요구조건 쌍 (Criterion Pair) | 의미적 연관 내용 (Semantic Chain) | Fineract (N=2,925)<br>공기수 / $\phi$ (p-value) | AI 벤치마크 (N=944)<br>공기수 / $\phi$ (p-value) | 표본 내 상관 양상 해석 |
| :--- | :--- | :---: | :---: | :--- |
| **$B_4 \leftrightarrow B_2$** | 소급 변경 $\leftrightarrow$ 수치 연쇄 재계산 | **254건 / $\phi = +0.430$** ($p < 10^{-94}$) | **5건 / $\phi = -0.013$** ($p = 0.825$) | **유의한 양의 상관 vs 상관 결여 ($\phi \approx 0$)** |
| **$A_1 \leftrightarrow B_4$** | 업무 규칙 $\leftrightarrow$ 시간적 소급 적용 | 471건 / $\phi = +0.309$ ($p < 10^{-71}$) | 42건 / $\phi = +0.024$ ($p = 0.496$) | Fineract 유의한 결합 vs AI 상관 미약 |
| **$A_1 \leftrightarrow B_2$** | 업무 규칙 $\leftrightarrow$ 복합 수치 산출 | 440건 / $\phi = +0.343$ ($p < 10^{-97}$) | 34건 / $\phi = +0.039$ ($p = 0.246$) | Fineract 유의한 결합 vs AI 상관 미약 |
| **$A_1 \leftrightarrow B_3$** | 업무 규칙 $\leftrightarrow$ 데이터 관계 정합성 | 538건 / $\phi = +0.329$ ($p < 10^{-79}$) | 115건 / $\phi = +0.094$ ($p = 0.005$) | 두 데이터셋 모두 유의한 결합 |
| **$B_2 \leftrightarrow B_3$** | 수치 재산출 $\leftrightarrow$ 원장 차대 정합성 | 189건 / $\phi = +0.226$ ($p < 10^{-29}$) | 14건 / $\phi = -0.007$ ($p = 1.000$) | Fineract 유의한 결합 vs AI 상관 미약 |
| **$B_3 \leftrightarrow B_6$** | 정합성 유지 $\leftrightarrow$ 상태 불변 보존 | 89건 / $\phi = +0.053$ ($p = 0.005$) | 63건 / $\phi = -0.106$ ($p = 0.001$) | AI 벤치마크 약한 음(-)의 상관 |
| **$B_4 \leftrightarrow B_3$** | 시간 소급 $\leftrightarrow$ 상태 정합성 | 138건 / $\phi = +0.069$ ($p = 0.0002$) | 22건 / $\phi = +0.022$ ($p = 0.501$) | Fineract 유의한 결합 vs AI 상관 미약 |
| **$B_4 \leftrightarrow B_6$** | 시간 소급 $\leftrightarrow$ 상태 보존 | 84건 / $\phi = +0.068$ ($p = 0.0005$) | 28건 / $\phi = -0.042$ ($p = 0.246$) | Fineract 유의한 결합 vs AI 상관 미약 |

* **통계 해석의 객관적 한계 및 관찰 사실**:
  - **Fineract의 상관 경향**: Fineract에서는 $B_4$(시간적 소급)와 $B_2$(수치 계산)가 254건 함께 공기하며, 통계적으로 유의미한 중간 수준의 양(+)의 선형 상관성($\phi = +0.430, p < 10^{-94}$)을 나타냅니다.
  - **AI 벤치마크의 상관 경향**: 반면 분석 대상 AI 벤치마크 944건 중 $B_4$와 $B_2$가 동시에 출현하는 과제는 **단 5건(0.53%)**에 불과하며, 상관계수는 $\phi = -0.013$ ($p = 0.825$)으로 0에 가깝게 관측됩니다.
  - **해석 수위 및 주의점**: $\phi = -0.013$은 해당 표본 내에서 두 조건 간의 선형적 공기 관계가 거의 존재하지 않는다는 경험적 관찰값이며, 두 속성이 수학적으로 완전 독립임을 의미하는 것은 아닙니다. 또한 이 상관계수 차이만으로 벤치마크의 과제 수집 프로세스 전체를 단일 원인으로 단정할 수 없으며, 분석된 벤치마크 과제들에서 소급 시간 처리와 정밀 수치 연산이 한 이슈 내에서 복합 결합되는 빈도가 금융 엔터프라이즈에 비해 현저히 낮게 나타난다는 실증적 차이로 이해되어야 합니다.
  - **방향성 의존관계의 별도 검증 필요성**: 따라서 이 통계적 공기 차이가 실제 소프트웨어 동작에서 어떠한 인과적 의미를 가지는지는, 4절의 Fineract 원문 의존관계와 5절의 AI 벤치마크 테스트 오라클 단언문 분석을 통해 미시적으로 규명합니다.

---

## 4. Fineract 16대 핵심 업무 의존관계 1:1 원문 증거 전수표 (Full Evidence Table)

Gate 2에서 원문 시작 오프셋 슬라이스 대조(20개 구절, 100% 일치)를 완료한 **Fineract 16대 핵심 업무 의존관계**([`gate2_dependencies.csv`](../data/gate2_dependencies.csv))의 전수 상세 증거표는 다음과 같습니다.

### [Table 4] Fineract 16개 핵심 업무 요구조건 의존관계 원문 및 인과 메커니즘 전수 대조표

| 의존 ID | 대상 이슈 (상태) | 의존 유형 | 정형 수식 | 원문 인용구 (`verbatim_raw_quote`) 및 시작 오프셋 | 쌍 인용구 (`paired_consequence_quote`) 및 시작 오프셋 | 도메인 인과 메커니즘 및 불변식 설명 |
| :---: | :---: | :---: | :---: | :--- | :--- | :--- |
| **DEP-01** | FINERACT-2338 (Resolved) | **Explicit** | $A_1 \rightarrow B_4$ | `"Backdate can be done on already paid Installments as well"` (pos: 261, len: 57) | `"Installments paid Interest amount will be reverse replayed as per the new Interest rate from the applied date"` (pos: 559, len: 109) | 기납부 회차에 대한 소급 이자율 변경 허용(A1)이 적용일 이후 기납부 회차의 연쇄 역분개 재처리(B4)를 직접 강제함. |
| **DEP-02** | FINERACT-2338 (Resolved) | **Explicit** | $B_4 \rightarrow B_2$ | `"Repayment schedule will be recalculated with New EMI and Interest from the Interest applied schedule date"` (pos: 325, len: 105) | N/A | 소급 재처리 실행 시 적용일 이후 상환 일정의 신규 EMI 및 이자 금액을 연쇄적으로 재산출함. |
| **DEP-03** | FINERACT-2338 (Resolved) | **Explicit** | $B_2 \rightarrow B_6$ | `"No of Installments will remain the same, only EMI and Interest would get affected"` (pos: 843, len: 81) | N/A | 개별 회차의 EMI와 이자가 변동되더라도 대출 계약의 총 상환 회차 수(No of Installments)는 불변 보존되어야 함. |
| **DEP-04** | FINERACT-2338 (Resolved) | **Explicit** | $B_4 \rightarrow B_3$ | `"If the repayment that was made before the charge-off is reversed and replayed due to backdated Interest modification,then the accounting entry of the reversed transaction and replayed transaction should follow *standard accounting rules and not charge-off accounting rules*"` (pos: 1005, len: 273) | N/A | 대손 상각(charge-off) 이전 거래가 소급 역분개될 때, 재처리 분개는 상각 규칙이 아닌 표준 회계 분개 규칙과의 관계 정합성을 유지해야 함. |
| **DEP-05** | FINERACT-753 (Resolved) | **Explicit** | $A_1 \rightarrow B_4, B_2$ | `"now reverse the deposit of 500 ...."` (pos: 1494, len: 32) | `"system will recalculateDailyBalances and reverse the charge transaction on this section of the code"` (pos: 1532, len: 99) | 과거 입금 거래 500 취소(A1) 시 직후 시스템이 `recalculateDailyBalances`를 호출하여 일일 잔액을 역산하고 연관 수수료를 연쇄 재계산함. |
| **DEP-06** | FINERACT-753 (Resolved) | **Explicit** | $B_4 \rightarrow B_3, B_6$ | `"now since the new charge created does not have the charged paid by object in the table \"  m_savings_account_charge_paid_by\" recalculating the account balance becomes wrong"` (pos: 2160, len: 171) | N/A | 잔액 재계산 과정에서 수수료 거래가 재생성될 때 `m_savings_account_charge_paid_by` 관계 링크가 누락되면 전체 계좌 잔액 원장이 오염됨. |
| **DEP-07** | FINERACT-2836 (In Progress) | **Explicit** | $B_7 \rightarrow B_6$ | `"Each due savings-charge installment is processed in an independent transaction."` (pos: 853, len: 79) | `"A successfully collected installment remains committed regardless of the outcome of another installment."` (pos: 1016, len: 104) | 각 회차별 수수료는 독립 트랜잭션으로 처리되어, 타 회차의 잔액 부족/실패 여부와 무관하게 성공 회차의 원장 커밋과 잔액 차감이 영속 보존됨. |
| **DEP-08** | FINERACT-2836 (In Progress) | **Inferred** | $B_7 \rightarrow B_3$ | `"Each due savings-charge installment is processed in an independent transaction."` (pos: 853, len: 79) | N/A | 회차별 독립 트랜잭션 경계 설정이 특정 회차 실패 시 전체 계좌 잔액 원장의 오염을 방지하기 위한 소프트웨어 아키텍처적 격리 조치임. |
| **DEP-09** | FINERACT-2836 (In Progress) | **Explicit** | $A_4 \rightarrow B_6$ | `"Re-running the job resumes from the first unpaid installment without collecting previously committed installments again."` (pos: 2293, len: 120) | N/A | 배치 스케줄러 재실행(A4) 시 이미 커밋된 이전 회차는 건너뛰고 첫 미납 회차부터 재개하여 멱등성 및 중복 징수 방지(B6)를 직접 강제함. |
| **DEP-10** | FINERACT-2836 (In Progress) | **Co-required** | $A_1, B_5 \rightarrow B_7, B_6$ | `"the job is not marked as failed solely because of the insufficient balance"` (pos: 1718, len: 74) | N/A | 특정 계좌의 잔액 부족은 시스템 예외가 아닌 정상 비즈니스 미납 상태(B5)로 격리되어, 전체 배치 작업을 실패 처리하지 않고 정상 완료함. |
| **DEP-11** | FINERACT-2930 (In Progress) | **Explicit** | $A_1 \rightarrow B_4$ | `"The loan is replayed from the earlier of the original and new transaction dates."` (pos: 2147, len: 80) | N/A | 과거 거래 일자/금액 정정 시 원 거래일과 신규 거래일 중 더 이른 날짜(earlier date)부터 후속 대출 거래 전체를 연쇄 소급 재처리함. |
| **DEP-12** | FINERACT-2930 (In Progress) | **Co-required** | $B_4 \rightarrow B_3, B_2, B_5$ | `"The schedule, balances, allocations, accruals and loan status (e.g. closed ↔ active, overpaid) are recalculated correctly."` (pos: 2228, len: 122) | N/A | 소급 재처리 결과로 상환 일정(schedule), 원장 잔액(balances), 상환 배분(allocations), 미수수익(accruals), 대출 상태(status) 5대 엔티티가 동시 재산출됨. |
| **DEP-13** | FINERACT-2930 (In Progress) | **Explicit** | $A_1 \rightarrow B_3$ | `"The new transaction stays linked to the same loan charge (LoanChargePaidBy / charge relation)."` (pos: 3368, len: 94) | N/A | 수수료 감면/조정 신규 거래는 일반 상환 거래로 취급되지 않고 원 수수료 엔티티(`LoanChargePaidBy`)와의 1:1 관계 링크를 엄격히 유지해야 함. |
| **DEP-14** | FINERACT-2930 (In Progress) | **Explicit** | $A_1, B_3 \rightarrow B_2$ | `"counting the reversed original as available again"` (pos: 3561, len: 49) | N/A | 신규 감면 금액은 수수료 가용 한도를 초과할 수 없으며, 취소된 원 거래 금액을 가용 한도로 재산입하여 상한선을 재계산함으로써 과다 감면을 방지함. |
| **DEP-15** | FINERACT-2930 (In Progress) | **Inferred** | $B_3, B_2 \rightarrow B_6$ | `"Journal entries are reversed for the original transaction and posted for the new one, using the correct accounts for that transaction type."` (pos: 2357, len: 139) | N/A | 거래 취소 및 신규 분개 전표 전기 후, 대출 계좌의 누적 원장 차변과 대변의 합계는 복식부기 회계 원리에 따라 정합성을 유지해야 함. |
| **DEP-16** | FINERACT-2934 (Open) | **Explicit** | $A_5 \rightarrow B_6$ | `"For installations that already configured both rows, the effective behaviour does not change."` (pos: 1527, len: 93) | N/A | 이중 설정 체계를 단일 구조로 통합하는 Liquibase DB 마이그레이션 실행 시 기존 설정값을 복제하여 기존 설치본의 유효 런타임 행위를 불변 보존함. |
| *(참조)* **DEP-SUPP-01** | FINERACT-977 (Resolved) | *Technical Reference* | $A_2 \rightarrow B_1$ | `"updateAmountsBasedOnCurrentEarlyPayments (AbstractLoanScheduleGenerator.java:640)"` (pos: 239, len: 81) | N/A | 조기 상환 재계산 시 내부 상환 일정 생성기 메서드 간의 연쇄 런타임 호출 스택트레이스 (기술적 참조 자료). |

---

## 5. AI 벤치마크 4대 비교 축 심층 정적 분석 증거 (Qualitative 4-Axis Evidence Analysis)

Gate 2에서 확정된 4대 비교 축([`gate2_case_mapping.csv`](../data/gate2_case_mapping.csv), [`gate2_harness_evidence.csv`](../data/gate2_harness_evidence.csv))에 대한 코드 diff 및 테스트 오라클 단언문 정적 분석 증거는 다음과 같습니다.

### [Table 5] AI 벤치마크 4대 사례별 요구조건 대비 평가 오라클 단언문 실측 대조표

| 비교 축 (Axis ID) | 과제 명세 상의 필수 요구조건 ($R_{spec}$) | 실제 평가 오라클의 검증 범위 ($R_{eval}$) | 검증 커버리지 ($C_{eval}$) | 의존관계 단절 분석 및 학술적 평가 |
| :--- | :--- | :--- | :---: | :--- |
| **Axis 1 (Direct Comparison)<br>NodeBB #0030** | **설정 데이터 이행 및 멱등성 ($A_5 \rightarrow B_6$)**:<br>기존 `restrictChat=1` 계정을 `chatAllowList`로 일괄 변환 이행하는 배치 스크립트(`src/upgrades/4.3.0/chat_allow_list.js`, 50라인) 작성 및 재실행 멱등성 요구. | **실시간 리프 권한 검사 단언 (`test/messaging.js:L103-121`)**:<br>`it('should respect allow/deny list...', ...)`<br>임시 mock 사용자(`User.create`)에게 메모리 상에서 직접 `chatAllowList`를 기입하고 리프 함수 `Messaging.canMessageUser()`만 단언. | **33.3% (1/3)**<br>(권한 판정만 검증) | **오라클 검증 범위 사각지대 (Construct Underrepresentation)**:<br>개발자 정답 diff(12개 파일)에는 50줄의 DB 마이그레이션이 포함되나, 결함 모델 diff(11개 파일)가 이를 완전히 빠뜨려도 테스트 스위트 전체에 업그레이드 스크립트 검증 코드가 전무(0건)하여 단언문 수준에서 감지되지 않음. |
| **Axis 2 (Scope Gap)<br>Element-Web #0139** | **시간적 소급 상태 전이 ($B_4 \rightarrow B_6$)**:<br>룸 타임라인과 스레드 타임라인 간에 읽음 영수증(receipt)이 역전 도착 시 미읽음 배지(badge) 소급 재계산 요구. | **인메모리 단위 상태 판정 (`test/Unread-test.ts`)**:<br>모의 객체(`mocked(haveRendererForEvent)`)를 통해 8개 이상의 인메모리 합성 이벤트 조합 상태 전이 분기 로직을 정밀하게 단언. | **33.3% (1/3)**<br>(인메모리 로직 한정) | **인메모리 단위 모킹과 영속 시스템 일관성의 층위 차이**:<br>단위 테스트로서 충실하나, 영속 IndexedDB 캐시 동기화나 네트워크 지연에 따른 서버 스트림 정합성은 평가 범위 밖임 (개발 목적과 평가 추상화 수준의 차이 규명). |
| **Axis 3 (Hierarchy Gap)<br>RocketMQ #0819** | **JVM 동시성 및 통계 정밀도 ($B_7, B_2$)**:<br>다중 스레드 경합 시 `StatsItemSet` 테이블 삽입 원자성(20,000L) 보장 요구. | **고강도 스레드 안전성 스트레스 테스트 (`StatsItemSetTest.java`)**:<br>100개 워커 스레드로 10,000개 작업을 50회 반복하여 JVM 공유 메모리 상의 `putIfAbsent` 원자적 누적을 엄밀하게 단언. | **100.0% (2/2)**<br>(단일 JVM 동시성 충족) | **단일 JVM 스레드 안전성과 업무 트랜잭션 격리의 층위 차이**:<br>단일 프로세스 원자적 연산($B_7$) 검증으로서는 매우 우수함. 그러나 이는 업무 트랜잭션 단위의 독립 트랜잭션 분리, 부분 실패 격리, 실패 시 성공 건 커밋 영속 보존(FINERACT-2836)과는 평가 층위가 다름. |
| **Axis 4 (Aligned Counterexample)<br>Navidrome #0495** | **DB 백업, 스키마 복원, 파일 정리 ($A_4, B_6, B_{10}$)**:<br>SQLite DB의 무중단 백업 파일 생성, 파괴적 DDL 삭제 후 백업 복원, 및 백업 파일 보존 개수 초과 시 오래된 파일 정리(Pruning) 요구. | **실제 DB 엔진 통합 테스트 (`db/backup_test.go`)**:<br>실제 SQLite 엔진 백업 생성, 파괴적 DDL(`DELETE FROM sqlite_master`), 복원 스키마 존재(`!isSchemaEmpty`), **백업 파일 보존 개수 및 Pruning(`len - pruneCount == expected`)**을 전면 단언. | **100.0% (3/3)**<br>(파일/엔진 레벨 충족) | **정합 반례로서의 긍정 평가 지평 확인**:<br>벤치마크가 실제 DB 엔진 조작과 파일 보존 정책을 성공적으로 검증할 수 있음을 입증하는 유의미한 긍정 반례임. 다만 단언문의 깊이가 파일/스키마 레벨에 한정되어 복합 비즈니스 엔티티 불변식까지는 요구하지 않음. |

---

## 6. 결론 및 후속 Gate 4 (논문 원고 집필) 연계 지침

본 Gate 3 증거 문서는 Gate 2에서 확보한 3대 실증 근거를 바탕으로 다음 사항을 체계적으로 완결했습니다:

1. **3대 벤치마크 패밀리 층화 지표의 객관화**:
   - SWE-bench Pro(731건, 다중 속성 출현 중심), PolyBench Java(165건, 단일 함수 중심), SWE-EVO(48건)의 실제 층화 통계를 확립하여, AI 벤치마크를 단일 집단으로 왜곡하지 않는 공정한 비교 기반을 마련했습니다.
2. **거시적 공기 통계와 미시적 인과 사슬의 방법론적 결합**:
   - 거시 통계($\phi$)를 통해 $B_4-B_2$의 대규모 코퍼스 공기 상관성 차이(+0.430 vs -0.013)를 수치화하고, 16개 Fineract 인과 사슬 및 NodeBB #0030 오라클 사각지대 분석을 통해 이를 코드 및 원문 수준에서 뒷받침했습니다.
3. **논문 본문(Gate 4) 배치 가이드라인**:
   - 본 문서의 **[Table 1]과 [Table 2]**는 논문 4장의 벤치마크 패밀리 층화 분석 표로 직접 배치합니다.
   - **[Table 3]**은 논문 5장의 거시적 상관계수 대조표로 배치합니다.
   - **[Table 4]와 [Table 5]**는 논문 5장의 정성 인과 사슬 및 4대 비교 축 분석 표로 배치합니다.

본 실증 데이터의 완결을 터미널 검증 스크립트([`scripts/09_verify_gate3.py`](../scripts/09_verify_gate3.py))를 통해 확인한 후, 마스터 실행 계획서의 최종 단계인 **Gate 4(CEUR-ART 12p 본문 원고 집필)**로 진입합니다.
