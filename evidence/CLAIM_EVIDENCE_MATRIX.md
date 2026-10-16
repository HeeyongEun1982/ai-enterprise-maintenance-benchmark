# Claim–Evidence Matrix (주장–증거 추적 매트릭스)
**문서 버전**: v0.4 최종 보완판  
**대상 문서**: `Paper/v0.4/paper_draft_v0.4_12p.md`  
**기준 데이터**: Gate 1~4 동결 데이터 (`Fineract N=2,925`, `AI N=944`, `Codebook 18-Criteria`, `E1 Matched Pairs N=1,177`, `Table 2~6`)  
**검증 일시**: 2026-10-16  

---

## 1. 개요 및 목적

본 매트릭스는 논문 `paper_draft_v0.4_12p.md`의 각 절(Section)별 핵심 학술적 주장(Claim)과 이를 뒷받침하는 구체적 실측 증거(Evidence), 증거의 유형(Evidence Type), 독립 검증 방식(Verification), 학술적 한계 및 경계(Limitation)를 1:1로 매핑하여 논문의 학술적 신뢰성과 추적 가능성(Traceability)을 보증한다.

---

## 2. 8개 장별 주장–증거 추적 매트릭스

| Section | Claim (핵심 주장) | Evidence (구체적 실측 증거) | Evidence Type | Verification (독립 검증 경로) | Limitation (학술적 한계 및 경계) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1.1** | AI 코딩 에이전트의 벤치마크 해결률(30~50%)과 실무 소프트웨어 유지보수 간에는 잠재적 평가·운영 불일치(Production Gap)가 존재한다. | SWE-bench Pro, PolyBench 리더보드 점수와 엔터프라이즈(Apache Fineract) 요구사항 특성 대조. | 문헌 및 벤치마크 리포트 실측치 | Jimenez et al. (2024), Fineract 공식 이슈 아카이브. | 특정 상용 에이전트의 실무 실패율을 직접 측정한 것이 아니며, 구조적 평가 타당성 간극으로 한정. |
| **1.3** | 분석된 F2P 테스트 패치의 정적 단언문이 다중 파일 아키텍처 요구(DB 마이그레이션)를 검증하지 않고 국소적 인메모리 리프 함수 단언문으로 한정하는 구조적 메커니즘이 관찰된다. | NodeBB #0030 개발자 정답 패치(12개 파일 수정, +383/-50 lines, 44줄 DB 마이그레이션 포함) vs `test/messaging.js` 인메모리 리프 권한 단언문. | 정적 코드 diff 및 테스트 코드 단언문 분석 | `Paper/v0.4/data_and_tables/ai_case_sources/` 및 원본 태스크 JSON 파싱. | 동적 패치 실행 결과나 런타임 하네스 전체에 대한 일반화가 아니며, 분석된 F2P 테스트 패치의 정적 단언문 범위 분석으로 엄밀히 한정. |
| **2.2** | 기존 벤치마크 감사 연구(SNC, UTBoost)는 저장소 위상 탐색이나 기존 테스트 클래스 내 패치 정답 판별력에 집중하여, 요구명세와 평가 오라클 간의 구성 타당도(Construct Validity)를 다루지 않았다. | SNC 3대 지표(Spread, Novelty, Centrality) 분석 및 UTBoost의 기존 테스트 파일 단위 단언문 증강 기법 원문 비교 (Table 1). | 선행 연구 문헌 감사 및 비교 매트릭스 | Shayanfar et al. (2025) \cite{shayanfar2025snc}, Yu et al. (2025) \cite{yu2025utboost}. | 기존 연구의 패치 판별력 개선 기여를 인정하며, 본 연구는 아키텍처 계층의 오라클 포함 여부 분석에 집중. |
| **2.3** | 본 연구는 요구사항을 활동($A$), 조건($B$), 방향성 의존 사슬로 분해하고, 명세 요구($R_{\text{spec}}$)와 오라클 단언 범위($R_{\text{eval}}$)를 직접 대조하는 새로운 분석 틀을 제공한다. | 18개 기준 분류체계, 3대 분석 층위 개념도 (Figure 1), 4대 분석 관점 정립. | 방법론적 프레임워크 | Section 2.3 본문 및 Table 1 Positioning Matrix. | 기존 연구가 요구사항을 전혀 보지 않았다고 단정하지 않고, 분석 단위와 평가 층위의 차별성으로 정의. |
| **3.1** | Apache Fineract 2,925건(3,811 단위)과 AI 벤치마크 944건(3,446 단위)의 전수 모집단을 구축하여 객관적 비교 기반을 마련했다. | Fineract 이슈 전수 아카이브(`raw_jira_issues`), AI 944개 태스크 원본(`comparison.json`: Pro 731, Poly 165, EVO 48). | 공식 전수 데이터셋 메타데이터 | `Paper/v0.4/scripts/10_verify_gate4.py` [검증 1] 전수 일치 확인. | Fineract 내 미해결/중복 티켓 한계를 명시하고, AI 벤치마크는 3대 계열 메타데이터 원천에 1:1 바인딩. |
| **3.2** | ISO 14764 및 ISO 25010에 기반하여 18개 기준 코드북을 구축하고, 1인 주연구자가 배치 단위로 3,446건을 코딩한 후 자동화 오프셋 검증 스크립트로 100% 무결성을 확보했다. | `framework-snapshot.json`, 944개 배치 스크립트(`batch_*.py`), 자동화 검증 보고서(`batch-*-check.json`, `validate_*.py`). | 동결 코드북 및 자동화 검증 스크립트 로그 | `RAW5/.../AB-CONTINUATION.txt`, `validate_0851_0944.py`. | 다수 연구자의 독립 이중 평가(IRR)가 아니며, 자동화 검증은 문자열 오프셋 일치를 보증한 것임을 6.1장에 명시. |
| **3.3** | 속성 다양성($\vert B \vert$), 통계적 공기($\phi$), 방향성 인과 사슬($A \rightarrow \Delta S \rightarrow B$)은 상호 대체 불가능한 독립된 3대 분석 층위이다. | FINERACT-753/2338 예시를 통한 3대 층위 개념도 (Figure 1). | 방법론적 분석 모델 | Section 3.3 및 Figure 1 텍스트 다이어그램. | 3대 층위를 속성 수가 오라클 누락을 유발한다는 식의 단일 선형 인과 사슬로 연결하지 않음. |
| **4.1** | 동일 네이티브 태그 및 파일 수와 strict tolerance churn 매칭 통제쌍에서도 57.4%는 요구조건 집합이 완전히 상이하여, 표면 메타데이터만으로 요구 복잡도를 설명할 수 없다. | 1,177개 통제 매칭쌍(Pro 714, Poly 463), 평균 Jaccard 거리 $\bar{d}_J=0.8138$, 676쌍(57.43%) $d_J=1.0000$. OpenLibrary #143 vs #233 실측 대조. | 통제 매칭쌍 정량 분석 | `data_and_tables/e1_matched_pairs.csv`, `scripts/10_verify_gate4.py` [검증 2]. | 벤치마크 설계자가 과제를 동일 난이도로 가정한다고 단정하지 않고, 표면 지표의 의미 설명 한계로 논증 한정. |
| **4.3** | SWE-bench Pro는 Fineract보다 평균 요구 속성 수($\vert B \vert$)가 통계적으로 유의하게 높다 (2.47 vs 1.78, $p = 4.29 \times 10^{-51}$). | Table 3 $\vert B \vert$ 9개 구간(0~8) 분포, Pro 평균 2.4733 vs Fineract 평균 1.7798, Welch's $t=15.78$. Pro의 85.09%가 $\vert B \vert \ge 2$. | 2표본 Welch $t$-검정 및 구간 분할표 | `data_and_tables/gate3_coupling_complexity.csv`, `scripts/10_verify_gate4.py` [검증 4]. | 요구 속성 수의 다양성이 높다는 사실이 하네스 오라클의 충실한 검증 깊이를 보증하지는 않음을 지적 (4.4장). |
| **5.1** | 거시적 상관계수($\phi$) 분석 결과, 기산일-이자 재계산 결합($B_4-B_2$)은 Fineract에서 강하게 결합($\phi=+0.430$)되나, AI 벤치마크에서는 5건만 출현하여 $\phi=-0.013$ ($p=0.825$)로 독립 기대치와 일치한다. | Table 4 11개 주요 의존 사슬 $\phi$ 상관 행렬, Fineract $B_4-B_2$ 254건 vs AI 5건 (AI 개별 빈도: $B_4$ 86건, $B_2$ 65건, 기대치 5.92건). | Pearson $\phi$ 및 Fisher's Exact Test | `data_and_tables/gate3_phi_correlation_matrix.csv`, `scripts/10_verify_gate4.py` [검증 5]. | $\phi \approx 0$은 독립 가정 하의 기대치와 일치함을 의미할 뿐 통계적 독립성의 절대 증명이 아니며, 도메인 차이는 인과적 원인이 아닌 맥락적 설명임. |
| **5.2** | Fineract 유지보수는 기능 변경이 후속 재계산을 유발하고 회계 불변식에 구속되는 16대 핵심 인과 의존관계를 엄격히 유지한다. | Table 5 16대 의존관계(DEP-01..DEP-16), FINERACT-2338/2930 등 Jira 원문 인용구 및 19개 슬라이스 바이트 단위 100% 일치. | 정성적 요구명세 원문 추적 | `data_and_tables/fineract/gate2_raw_source_snippets.json`, `scripts/09_verify_gate3.py` [검증 4]. | 금융 코어뱅킹의 엄격한 복식부기 및 규제 불변식이 반영된 결과이므로 일반 소프트웨어로 무리하게 일반화하지 않음. |
| **5.3 (Axis 1)** | NodeBB #0030: DB 마이그레이션은 명세서의 Explicit Requirement이자 정답 패치의 Developer Obligation이나, 분석된 F2P 테스트 패치(`test/messaging.js`)는 인메모리 리프 권한만 직접 단언하여 마이그레이션 직접 단언문이 부재한다. | 명세서(`requirements`, `interface`), 44줄 배치 마이그레이션 코드(`src/upgrades/4.3.0/chat_allow_list.js`) vs `test/messaging.js:L103-121`. | 소스 코드 diff 및 테스트 코드 단언문 대조 | `data_and_tables/ai_case_sources/` 및 Table 6 Row 1. | 런타임 하네스 전체가 마이그레이션을 탐지하지 못한다는 일반화가 아니며, 분석된 F2P 테스트 코드에 마이그레이션 직접 단언문이 0건이라는 정적 단언 범위로 한정. |
| **5.3 (Axis 2)** | Element-Web #0139: 스레드 읽음 계산은 Explicit Requirement이나, IndexedDB 영속 동기화는 Inferred Requirement이며, 단위 테스트(`test/Unread-test.ts`)는 Mock 상태 전이만 검증한다. | 명세 원문(`requirements`), `src/Unread.ts` 구현 vs `test/Unread-test.ts` 내 `mocked(haveRendererForEvent)`. | 소스 코드 diff 및 테스트 단언문 대조 | `Paper/v0.4/data_and_tables/ai_case_sources/0139.json`, Table 6 Row 2. | 명세에 명시되지 않은 IndexedDB 동기화를 테스트가 검증하지 않는다고 해서 부당한 오라클 결함으로 과장하지 않음. |
| **5.3 (Axis 3)** | RocketMQ #0819: JVM 레벨 멀티스레드 동시성은 Explicit Requirement이며, 평가 테스트(`StatsItemSetTest.java`)가 100 스레드로 원자성을 충실히 직접 검증한다. | `problem_statement`, `StatsItemSet.java` 내 `putIfAbsent` 구현 vs `StatsItemSetTest.java` 100 워커 스레드 및 20,000L 단언문. | 소스 코드 diff 및 테스트 단언문 대조 | `Paper/v0.4/data_and_tables/ai_case_sources/0819.json`, Table 6 Row 3. | 분산 트랜잭션 경계 미검증은 명세 외 범위이므로 결함이 아니며, 단일 JVM 멀티스레드 동시성 요구의 적합한 검증 사례로 정립. |
| **5.3 (Axis 4)** | Navidrome #0495: SQLite 온라인 백업, 파괴적 DDL 복원, 파일 보존 정책은 Explicit Requirement이며, 엔진 통합 테스트(`db/backup_test.go`)가 이를 엔드투엔드로 완벽 검증한다. | `problem_statement`, `requirements`, `cmd/backup.go` 구현 vs `db/backup_test.go` 내 `DELETE FROM sqlite_master` 및 파일 보존 단언문. | 통합 테스트 코드 파싱 및 단언문 대조 | `Paper/v0.4/data_and_tables/ai_case_sources/0495.json`, Table 6 Row 4. | 벤치마크에서도 상태형 컨테이너 환경이 구비되면 영속 상태 불변식을 충실히 평가할 수 있음을 입증하는 모범적 반례로 제시. |
| **6.1** | 1인 주연구자 주석 및 자동화 오프셋 검증의 한계(다자 일치도 부재)를 투명하게 인정하고, 동결 코드북과 전수 원문 인용구 공개를 통해 주관적 편향을 통제했다. | Section 6.1 한계 서술, 3,446개 인용구 공개, `validate_*.py` 검증 보고서. | 내부 타당도 위협 선언 | Section 6.1 본문. | 다자 간 상호 일치도(Cohen's $\kappa$ 등)를 주장하지 않으며, 텍스트 오프셋 검증과 의미적 분류 정확도를 엄격히 구별. |
| **6.2** | 본 연구의 정성적 오라클 분석은 정적 코드 단언문 분석에 기반하며, 미실행 모델에 대한 동적 실행 성공률이나 벤치마크 전반의 실패 빈도로 일반화하지 않는다. | Section 6.2 외부 타당도 선언문 (정적 단언문 분석 vs 동적 해결률 구분). | 외부 타당도 및 일반화 한계 | Section 6.2 본문. | 가상의 실행 로그(`report.json` 등)를 일체 배제하고, 하네스의 구조적 단언 가능 범위 분석으로 엄밀히 한정. |
| **7.1** | 코드 Churn이나 파일 수 등 표면 메타데이터는 요구조건의 의미적 차이를 설명하지 못하며, 속성 개수만이 아닌 평가 오라클의 검증 범위가 핵심 차원이다. | E1의 Jaccard 거리($\bar{d}_J=0.8138$, 57.4% 완전 불일치) 및 E2의 정적 오라클 단언 범위 분석 결과 종합. | 정량·정성 종합 논의 | Section 7.1 본문. | 벤치마크 설계자의 주관적 가정을 임의로 추정하지 않고, 실측 관찰에 기초한 학술적 함의로 서술. |
| **7.2** | 레거시 데이터 보존 및 마이그레이션 요구 과제에 대한 상태형 테스트베드 도입, 계층적 불변식 검증, 계층화된 의존성 보고를 원칙적 벤치마크 설계 함의로 도출한다. | NodeBB #0030(미검증) vs Navidrome #0495(검증 완료) 대조 및 Fineract 16대 의존관계 분석 결과. | 원칙적 설계 함의 | Section 7.2 본문. | 모든 벤치마크에 영속 DB가 필요하다는 식의 과도한 처방을 배제하고, 요구조건 특성에 부합하는 테스트베드 선택을 제안. |
| **8.0** | 3대 연구 질문(RQ1, RQ2a, RQ2b)에 대해 실측 데이터에 기반한 명확한 해답을 제시하며, 향후 서비스 컴퓨팅 벤치마크의 평가 타당성 제고 방향을 정립한다. | 본문 전체 실측치(RQ1: 매칭쌍 $d_J=0.8138$, Pro $\vert B \vert=2.47$; RQ2a: $\phi=+0.430$ vs $-0.013$; RQ2b: 오라클 단언 범위 분리) 총괄. | 연구 총괄 결론 | Section 8 본문. | 데이터에 기초한 결론만을 제시하며, 확인되지 않은 가설이나 미실측 성능 주장을 일체 배제. |

---

## 3. 검증 범위 구분: 자동화 계산 무결성 vs. 학술적 구성 타당도

본 매트릭스의 검증은 다음 두 가지 층위로 엄격히 구분되며, 모든 주장의 학술적 타당성이 완벽히 검증되었다고 선언하지 않는다:

### 1) 자동화 무결성 검증 (Automated Integrity Verification) — PASS
- **검증 대상**: 원천 자료와의 1:1 일치, 통계량 재계산, 텍스트 인용구 및 파일 해시 일치.
  - **원문 JSON 아카이브**: `RAW5/.../tasks/*.json`, `Paper/v0.4/data_and_tables/ai_case_sources/*.json`
  - **통계 데이터 CSV**: `e1_matched_pairs.csv`, `gate3_stratified_family_metrics.csv`, `gate3_coupling_complexity.csv`, `gate3_phi_correlation_matrix.csv`, `gate2_dependencies.csv`
  - **자동화 검증 스크립트**: `scripts/10_verify_gate4.py` 및 `scripts/09_verify_gate3.py` 실행 결과 **전수 PASS (0 Failures, Exit Code 0)**.
- **보증 범위**: 본문의 표, 통계 수치, 바이트 오프셋, 금지 어휘 배제 등 계산적·기술적 무결성을 100% 보증함.

### 2) 학술적 의미 및 구성 타당도의 경계 (Academic Interpretive Scope)
- **해석적 한계**: 자동화 스크립트의 `PASS`는 데이터의 정합성과 무결성을 입증할 뿐, 정성적 코드 해석, 도메인 아키텍처 맥락, 벤치마크 설계 평가에 대한 학술적 논증 전체가 반박 불가능하게 "완벽 증명"되었음을 의미하지 않음.
- **타당성 경계**: 1인 주연구자 주석에 따른 Inter-coder reliability 부재, Apache Fineract의 코어뱅킹 도메인 특수성, F2P 테스트 코드의 정적 단언문 분석 범위 등은 Section 6(Threats to Validity)에 명시된 한계 내에서 엄밀히 제한적으로 해석되어야 함.
