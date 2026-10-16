# 스토리라인 검증 보고서 (Storyline Verification Report)
**문서 버전**: v0.4 최종 보완판 (정합성 최종 수정)  
**대상 문서**: `Paper/v0.4/paper_draft_v0.4_12p.md` 및 `Paper/전체_작업_계획서.md`  
**기준 데이터**: Gate 1~4 동결 데이터 (`Fineract N=2,925`, `AI N=944`, `Codebook 18-Criteria`, `E1 Matched Pairs N=1,177`, `Table 2~6`)  
**검증 일시**: 2026-10-16  

---

## 1. 개요 및 목적

본 보고서는 `paper_draft_v0.4_12p.md` 원고에 대해 논문의 논리적 연결성, 학술적 독창성, 방법론의 신뢰성, 주장과 증거의 일치성을 강화하기 위한 최종 스토리라인 보완 결과를 검증하고 기록한다. 새로운 실험이나 가공 데이터를 생성하지 않고, 기존 Gate 1~4에서 검증된 확정 통계와 정적 코드 증거에 기초하여 심사위원의 핵심 지적 사항을 체계적으로 해결하였다.

---

## 2. 5대 필수 수정 사항 전·후 대조 및 변경 사유

### P0-1. Section 3.2 — 실제 Annotation 수행 절차 검증 및 투명화

* **수정 전 문장 (Section 3.2)**:
  > *"Software engineering researchers then manually performed semantic coding, binding each of the 3,446 criteria assignments to verbatim text quotes and commit diff line spans. Ambiguous cases were resolved through joint adjudication against the frozen definitions in `framework-snapshot.json`."*
* **수정 후 문장 (Section 3.2 & 6.1)**:
  > **Section 3.2**: *"Semantic coding across the 944 AI benchmark tasks was conducted through an iterative batch annotation protocol. For each task, the raw `problem_statement`, `requirements`, and `interface` specifications were individually examined by the primary investigator to identify explicit maintenance activities and required completion invariants according to the operational rules above. Each of the 3,446 criteria assignments was bound to a verbatim textual quote and explanatory rationale within modular batch scripts. To eliminate transcription drift and prevent ungrounded claims, an automated verification pipeline (`validate_*.py`) programmatically verified every assignment by checking contiguous task ID sequences, source file hashes, exact string offsets/quotes against raw source JSON files, and strict schema compliance against the frozen codebook in `framework-snapshot.json`. We emphasize that this automated verification confirms textual quotation fidelity, hash integrity, and codebook adherence rather than consensus across multiple independent human raters. The absence of multi-coder reliability statistics is explicitly documented as a construct threat in Section 6.1."*  
  > **Section 6.1**: *"First, semantic coding across the 944 AI benchmark tasks was conducted by a single investigator rather than independent double-blind coders, and boundary cases were resolved against the frozen codebook definitions rather than a multi-researcher joint adjudication committee. Although all 3,446 criteria assignments were validated through automated verification scripts (`validate_*.py`), programmatic offset checking guarantees textual quotation fidelity and source hash integrity rather than multi-coder reliability. As previously documented, no formal multi-annotator agreement study was conducted, and we make no claim of dual-coder consensus statistics."*
* **변경 이유**:
  - 실제 수행 기록(`RAW5/.../AB-CONTINUATION.txt`, `batch_*.py`, `validate_*.py`) 전수 감사 결과, 944개 과제는 1인 주연구자가 순차 배치 스크립트를 작성하여 원문 인용구를 바인딩하고 자동화 검증 스크립트로 오프셋/해시 일치를 확인한 것으로 확인됨.
  - 복수 연구자의 독립 이중 평가나 위원회식 공동 판정 기록이 존재하지 않으므로, 수행하지 않은 절차를 사실로 주장하지 않고 연구 수행의 실제 과정을 정직하고 투명하게 서술함.
  - 과거 철회된 $\kappa=0.9100$을 전면 배제하고, 문자열 오프셋 일치와 의미적 라벨 정확도(Inter-coder reliability)의 개념적 차이를 명확히 분리하여 6.1장 한계로 고백함.
* **근거 파일**:
  - `RAW5/03_AI944개_전체_비교평가/comparison/maintenance18-ai944/AB-CONTINUATION.txt`
  - `RAW5/03_AI944개_전체_비교평가/comparison/maintenance18-ai944/batch_0036_0040.py` ... `batch_0921_0944.py`
  - `RAW5/03_AI944개_전체_비교평가/comparison/maintenance18-ai944/validate_0851_0944.py`
  - `Paper/v0.4/data_and_tables/framework-snapshot.json`

---

### P0-2. Section 5.3 & 8 — 4개 비교 사례의 요구조건 출처(Provenance) 구분 및 결론 분리

* **수정 전 문장 (Section 5.3 Table 6 및 본문)**:
  > $R_{\text{spec}}$에 대해 요구조건의 출처 구분 없이 "Database Migration & Idempotency", "Temporal State Synchronization" 등으로 포괄 서술하여, 이슈 원문 명세에 직접 포함된 조건과 연구자가 운영 현실을 고려해 추론한 조건이 혼동될 여지가 있었음. 또한 결론에서 NodeBB와 Element-Web을 동일한 "construct underrepresentation"으로 묶었음.
* **수정 후 문장 (Section 5.3 Table 6, 본문 및 Section 8)**:
  > **본문 도입부**: *"Furthermore, to rigorously distinguish between what was directly demanded by the benchmark task and what was implemented or inferred, we categorize requirement conditions into three explicit provenance categories:  
  > 1. **Explicit Requirement**: A condition directly stated in the issue description, formal requirements list, or interface specification.  
  > 2. **Developer-Implemented Obligation**: A concrete implementation artifact present in the reference developer patch to fulfill system behavior.  
  > 3. **Inferred Requirement**: An operational system condition deduced from production architectural realities, but not explicitly requested in the task prompt."*  
  > **Axis 1 (NodeBB #0030)**: $R_{\text{spec}}$는 **Explicit Requirement & Developer Obligation** ($A_5 \rightarrow B_6$). 명세서(`requirements`: *"Provide an upgrade path should populate chatAllowList from each user's follow list..."*, `interface`: `src/upgrades/4.3.0/chat_allow_list.js`)의 명시적 요구이며 개발자 정답 패치에서 44줄 배치 마이그레이션 코드(새 파일 44 LOC, unified diff 청크 50줄)로 확인됨. 분석된 테스트 코드(`test/messaging.js:L103-121`)는 인메모리 리프 권한(`Messaging.canMessageUser()`)만 단언하여 마이그레이션이 완전히 미검증됨.  
  > **Axis 2 (Element-Web #0139)**: 스레드 타임라인별 읽음 영수증 계산은 **Explicit Requirement & Developer Obligation** (`src/Unread.ts`). 반면 Persistent IndexedDB 캐시 동기화는 프로덕션 실환경의 **Inferred Requirement**임. 단위 테스트(`test/Unread-test.ts`)가 인메모리 Mock 상태 전이를 검증하고 영속 동기화는 검증 범위 밖임을 구별 기술하여, 원문에 없는 요구를 오라클이 검증하지 않았다고 해서 부당한 오라클 결함으로 몰지 않음.  
  > **Axis 3 (RocketMQ #0819)**: JVM 레벨 멀티스레드 동시성(`StatsItemSet`, 20,000L)은 **Explicit Requirement & Developer Obligation** (`putIfAbsent`). 테스트 코드(`StatsItemSetTest.java`)가 100 워커 스레드로 이를 직접 검증함. 분산 트랜잭션 경계 미검증은 명세 외 범위이므로 결함이 아닌 JVM 동시성 충족 사례로 서술함.  
  > **Axis 4 (Navidrome #0495)**: SQLite 온라인 백업, 파괴적 DDL 복원, 파일 보존 정책은 **Explicit Requirement & Developer Obligation** (`cmd/backup.go`, `db/backup.go`). 테스트 코드(`db/backup_test.go`)가 `DELETE FROM sqlite_master` 및 파일 보존 개수를 엔드투엔드로 완벽 검증하는 모범적 정렬 사례로 정립함.  
  > **Section 8 Conclusion RQ2b**: NodeBB와 Element-Web을 동일한 결함으로 묶지 않고, NodeBB는 **"명시적 요구조건(Explicit Requirement)의 오라클 검증 누락"**으로, Element-Web은 **"Mock 단위 검증과 추론된 영속 상태 조건(Inferred Requirement)의 범위 경계"**로 명확히 분리 서술함.
* **변경 이유**:
  - 4개 사례의 명세 원문(`problem_statement`, `requirements`, `interface`), 정답 패치(`patch`), 평가 테스트(`test_patch`)를 1:1 대조하여 각 요구의 출처를 3단계로 엄격히 구분함.
  - NodeBB 마이그레이션 코드의 실제 길이(새 파일 44 LOC)와 패치 diff 청크 크기(50줄)를 명확히 구분하여 서술 전체의 수치를 44 LOC로 통일함.
  - 요구되지 않은 추가 시스템 기능(예: RocketMQ의 분산 트랜잭션, Element-Web의 IndexedDB 영속 동기화)을 테스트가 검증하지 않는다는 이유만으로 평가 결함이라고 단정하는 오류를 원천 차단함.
* **근거 파일**:
  - `RAW5/03_AI944개_전체_비교평가/comparison/se-ai-comparison/tasks/0030.json`
  - `Paper/v0.4/data_and_tables/ai_case_sources/0139.json`
  - `Paper/v0.4/data_and_tables/ai_case_sources/0819.json`
  - `Paper/v0.4/data_and_tables/ai_case_sources/0495.json`

---

### P1-1. Section 2 — 선행연구(UTBoost, SNC, SWE-bench 감사)와의 비교 정밀화 및 독창성 방어

* **수정 전 문장 (Section 2.2~2.3)**:
  > 기존 감사 연구가 단위 테스트 취약성에만 집중하고 요구사항-오라클 일치성을 전혀 고려하지 않았다는 식의 다소 단정적인 서술이 존재했음.
* **수정 후 문장 (Section 2.2~2.3)**:
  > **Section 2.2**: *"Recent benchmark audits have investigated test suite reliability, focusing primarily on four key analytical perspectives: (1) Patch correctness discrimination: Evaluating whether test suites reliably distinguish correct developer fixes from plausible but incorrect agent patches. (2) Test suite fragility: Identifying sparse assertion density or missing edge-case assertions in pre-existing test files. (3) Test flakiness: Pinpointing non-deterministic test outcomes or environment execution instability. (4) Benchmark specification incompleteness: Examining linguistic ambiguity or underspecified context in natural language issue prompts. Specifically, UTBoost addresses assertion fragility by synthesizing additional unit tests within existing test suites to enhance patch-correctness discrimination... Without disputing the value of prior test augmentation techniques, our work investigates structural evaluation construct validity, examining whether benchmark test suites possess the construct coverage to evaluate the operational system invariants mandated by task specifications."*  
  > **Section 2.3**: *"In contrast, this paper investigates the semantic contract of the Definition of Done (DoD) across four distinct, non-fungible analytical perspectives: (1) Ontological separation of activities and conditions ($A$ vs. $B$)... (2) Disentangling co-presence from directed dependency ($|B|$ vs. $A \rightarrow \Delta S \rightarrow B$)... (3) Direct specification-to-oracle mapping ($R_{\text{spec}}$ vs. $R_{\text{eval}}$)... (4) Operational state invariant coverage (persistent schema migrations, financial balance preservation vs. localized in-memory mocking)."*
* **변경 이유**:
  - 기존 선행연구(UTBoost, SNC, SWE-bench Audit)의 학술적 기여(패치 변별력, 테스트 플레이크, 프롬프트 모호성)를 객관적으로 인정하고 경의를 표함.
  - 본 연구가 제공하는 독창적인 4대 분석 관점을 상호 보완적인 구성 타당도(Construct Validity) 차원에서 명확히 대비시킴.
  - 가상의 참고문헌을 일체 생성하지 않고, 실제 확인된 문헌(\cite{jimenez2024swebench}, \cite{chen2021codex}, \cite{xia2024sweevo}, \cite{shayanfar2025snc}, \cite{yu2025utboost})만 정확히 인용함.
* **근거 파일**:
  - `Paper/v0.4/paper_draft_v0.4_12p.md` (Section 2.2, 2.3, Table 1, References)

---

### P1-2. Section 5.1 — $\phi$ 상관계수의 올바른 통계적 해석 및 도메인 서술 수위 조절

* **수정 전 문장 (Section 5.1)**:
  > *"near-zero correlation indicates that criteria rarely co-occur in the AI benchmark corpus..."*
* **수정 후 문장 (Section 5.1)**:
  > *"We emphasize that Pearson's $\phi$ measures linear co-occurrence within issue specifications across the corpus; a near-zero $\phi$ coefficient indicates that two criteria co-occur at a rate consistent with statistical independence given their individual marginal frequencies, rather than establishing an absolute absence of criteria or a directed causal relation...  
  > **Statistical Insight & Calibration of $\phi \approx 0$**: In Apache Fineract ($N=2,925$), temporal backdating ($B_4$, 520 issues, 17.78%) and numerical calculation ($B_2$, 452 issues, 15.45%) co-occur in **254 issues (8.68%)**. This substantially exceeds the co-occurrence expected under independence ($(520 \times 452)/2,925 \approx 80.35$ issues), yielding a statistically significant moderate positive linear correlation ($\phi = +0.430, p < 10^{-90}$). In contrast, across the 944 AI benchmark tasks, $B_4$ occurs in 86 tasks (9.11%) and $B_2$ occurs in 65 tasks (6.89%), but they co-occur in **only 5 tasks (0.53%)**. Statistically, $\phi = -0.013$ ($p = 0.825$, Fisher's exact test) does not indicate that criteria rarely occur individually, nor does it prove absolute statistical independence across all possible software contexts. Rather, it demonstrates that their joint occurrence rate ($5/944$) closely aligns with the expected baseline frequency under statistical independence ($(86 \times 65)/944 \approx 5.92$). Thus, within the benchmark corpus, the presence of temporal requirements provides no linear predictive information regarding numerical recalculation requirements. While domain differences provide a plausible explanation for this divergence—financial platforms inherently bind retroactive effective dates to ledger recalculations, whereas general-purpose open-source libraries often modularize scheduling and arithmetic into independent subsystems—this architectural difference should be interpreted as a domain contextualization rather than a causally proven deterministic driver."*
* **변경 이유**:
  - $\phi \approx 0$은 두 조건이 독립일 때의 기대 결합 확률과 일치함을 의미할 뿐, 개별 조건의 출현 빈도가 낮다는 것을 의미하지 않음($B_4$ 86건, $B_2$ 65건).
  - 통계적 독립성이 "완벽히 증명"되었다는 인상을 주는 단정적 표현을 배제하고, 실측 수치($5/944$, 기대값 $5.92$, $p=0.825$)를 명확히 제시함.
  - 금융과 일반 소프트웨어의 도메인 특성 차이를 데이터로 직접 입증된 인과적 원인이 아니라, 설득력 있는 아키텍처적 도메인 맥락(Architectural Contextualization)으로 수위를 조절함.
* **근거 파일**:
  - `Paper/v0.4/data_and_tables/gate3_phi_correlation_matrix.csv`
  - `Paper/v0.4/paper_draft_v0.4_12p.md` (Table 4)

---

### P1-3. Section 7.1 — E1 결과의 객관적 서술 및 빈도 일반화 표현 교정

* **수정 전 문장 (Section 7.1)**:
  > *"Current benchmarks treat tasks with identical churn as equivalent, overlooking massive differences in operational state dependencies."*  
  > *"their automated evaluation harnesses often truncate these requirements into localized leaf helper function assertions."*
* **수정 후 문장 (Section 7.1)**:
  > *"The findings of this paper demonstrate that software maintenance complexity cannot be adequately characterized solely by surface metadata such as lines of code churn or file navigation graphs. In our controlled matched-pair experiment (E1), across 1,177 pairs sharing identical native types, modified file counts, and churn volumes, tasks exhibited an average Jaccard distance of 0.8138 over their fulfillment condition sets, with 57.4% (676 pairs) possessing completely disjoint requirements ($d_J = 1.0000$). This empirical evidence confirms that surface repository metrics alone are insufficient to account for the substantial semantic differences in requirement fulfillment conditions across maintenance tasks."*  
  > *"Furthermore, our demonstration that SWE-bench Pro tasks exhibit higher attribute diversity ($|B|=2.47$) than Apache Fineract ($1.78$) indicates that **attribute count alone is insufficient to characterize evaluation validity, and evaluation oracle construct coverage represents a critical additional dimension in assessing maintenance capability**. As demonstrated across our qualitative case analyses, an automated evaluation harness may restrict its verification to localized leaf helper functions, leaving operational state transformations (such as database migrations) outside its directly asserted scope."*
* **변경 이유**:
  - E1이 검증한 것은 "동일한 Churn, 파일 수, 네이티브 태그를 가진 1,177개 매칭쌍에서 요구조건의 Jaccard 거리가 0.8138에 달하고 57.4%가 완전 불일치한다"는 실측 사실임. 벤치마크 설계자의 주관적 가정을 비약하지 않고 표면 지표의 설명 한계로 서술을 정돈함.
  - 4개 정성 사례를 근거로 벤치마크 전반에 'often truncate'가 일어난다는 빈도 일반화 표현을 제거하고, 정성 사례 분석에서 관찰된 현상으로 엄밀히 한정함.
* **근거 파일**:
  - `Paper/v0.4/data_and_tables/e1_matched_pairs.csv`
  - `Paper/v0.4/paper_draft_v0.4_12p.md` (Section 4.1, 7.1)

---

## 3. 8개 장별 핵심 주장 및 지원 증거 체계 (Chapter-by-Chapter Core Claims)

| 장 (Section) | 핵심 연구 주장 (Core Claim) | 지원 실측 증거 (Supporting Evidence) | 증거 유형 및 위치 |
| :--- | :--- | :--- | :--- |
| **1. Introduction** | AI 코딩 에이전트의 벤치마크 해결률과 실무 소프트웨어 유지보수 간에 보고되는 잠재적 평가·운영 불일치(potential evaluation-to-production mismatch)에 대해, 단순 코드 크기 대신 요구조건 의미 구조와 평가 하네스의 구성 타당도(Construct Validity) 관점에서 구조적 메커니즘을 분석한다. | NodeBB #0030의 44줄 DB 마이그레이션 스크립트(44 LOC, unified diff 청크 50줄)가 정답 패치에 존재하나 분석된 F2P 평가 테스트(`test/messaging.js`)는 인메모리 리프 권한만 직접 단언하여 마이그레이션이 미검증되는 정적 대조 사례 제시(전체 런타임 하네스 일반화 배제). | 정적 코드 diff 및 커밋 diff (`ai_case_sources/`) |
| **2. Related Work** | 기존 벤치마크 감사 연구(SNC, UTBoost)가 저장소 탐색 및 기존 테스트 파일 내 패치 정답 판별력에 집중한 반면, 본 연구는 요구사항을 활동($A$)과 조건($B$)으로 분해하고 평가 오라클의 아키텍처 불변식 검증 범위를 분석한다. | UTBoost(Yu et al., 2025), SNC(Shayanfar et al., 2025) 등 원문 서지 1:1 대조 및 Table 1 비교 매트릭스. | 선행 연구 문헌 감사 (`paper_draft_v0.4_12p.md:Table 1`) |
| **3. Methodology** | ISO 14764(유지보수 활동) 및 ISO 25010(품질 속성)에 기반한 18개 기준 코드북을 구축하고, 3대 분석 층위(속성 다양성, 통계적 공기, 방향성 인과 사슬)를 통해 평가 타당성을 체계적으로 측정한다. Figure 1은 FINERACT-753/2338의 예시적 합성(Illustrative Synthesis)을 통해 3대 층위를 설명한다. | Fineract 전수 2,925건(3,811 단위)에서 도출 및 동결된 `framework-snapshot.json`, AI 944건 전수 3,446개 항목 배치 주석 및 `validate_*.py` 바이트 오프셋 검증. | 동결 코드북 및 배치 검증기 (`framework-snapshot.json`) |
| **4. E1: Surface Metadata vs. Semantic Complexity** | 동일 Churn, 파일 수, 태그를 가진 과제라도 요구조건의 의미적 집합은 완전히 상이하며, SWE-bench Pro는 Fineract보다 평균 요구 속성 수($\vert B \vert$)가 유의하게 높다(2.47 vs 1.78, $p < 10^{-50}$). | 1,177개 통제 매칭쌍($\bar{d}_J=0.8138$, disjoint 57.4%), Table 2 계열별 층화 통계, Table 3 $\vert B \vert$ 9개 구간 분포 및 Welch $t=15.78$. | 통제 매칭쌍 CSV 및 Welch 검정 (`e1_matched_pairs.csv`, `Table 2~3`) |
| **5. E2: Requirement Dependency & Evaluation Oracle** | 거시적 상관계수($\phi$)의 도메인별 분리와 미시적 인과 사슬(Fineract 16대 사슬)을 규명하고, AI 벤치마크 평가 하네스가 명세 요구 중 어떤 계층을 직접 단언하는지 4개 축으로 실증한다. | Table 4 $\phi$ 상관 행렬($B_4-B_2$: Fin +0.430 vs AI -0.013), Table 5 16대 Fineract 의존관계 Jira 원문 바이트 일치, Table 6 4대 비교 축(NodeBB, Element-Web, RocketMQ, Navidrome). | 공기 행렬 CSV, Jira 원문 슬라이스, 태스크 JSON (`Table 4~6`) |
| **6. Threats to Validity** | 1인 주연구자 배치 분류 및 자동화 오프셋 검증의 한계(다자 일치도 부재), 금융 도메인의 특수성, 정적 하네스 단언문 분석의 범위를 투명하게 고백하여 연구의 타당성 경계를 설정한다. | Section 6.1 내부 타당도(1인 주석, 오프셋 검증 vs 의미 일치도 한계 고백), Section 6.2 외부 타당도(미실행 동적 해결률 주장 배제, 일반화 한계 명시). | 원고 내 한계 고백 절 (`paper_draft_v0.4_12p.md:Section 6`) |
| **7. Discussion & Implications** | Churn 중심의 복잡도 패러다임을 극복하고, 요구조건에 부합하는 상태형 테스트베드 도입, 다계층 불변식 검증, 계층화된 벤치마크 평가 지표 설계를 원칙적 설계 함의로 제안한다. | E1의 실측 불일치($d_J=0.8138$) 및 Navidrome #0495의 SQLite 엔진 통합 테스트 성공 사례를 근거로 한 원칙적 도출. | 정성·정량 통합 함의 (`paper_draft_v0.4_12p.md:Section 7`) |
| **8. Conclusion** | 3대 연구 질문(RQ1, RQ2a, RQ2b)에 대한 명확한 실측 답변을 제시하되, RQ2b에서 NodeBB(분석된 F2P 테스트 패치 내 명시적 DB 마이그레이션 직접 단언문 부재)와 Element-Web(Mock 단위 검증과 추론된 영속 동기화의 범위 차이)을 범주별로 명확히 분리하여 총괄 정리한다. | RQ1(매칭쌍 $d_J=0.8138$, Pro $\vert B \vert=2.47$), RQ2a($B_4-B_2$ $\phi=+0.430$ vs $-0.013$), RQ2b(하네스별 오라클 검증 범위 분리) 실측치 총괄. | 결론 및 요약 (`paper_draft_v0.4_12p.md:Section 8`) |

---

## 4. 해결된 심사위원 지적 사항 요약

1. **"NodeBB 마이그레이션 코드 길이 충돌(50줄 vs 44줄)" 해결**:
   - 원본 패치 diff 파싱 결과, 신규 생성된 `chat_allow_list.js`의 실제 코드 줄 수는 **44 LOC**이며, git diff 청크 줄 수가 **50줄**(헤더 6줄 + 코드 44줄)임을 확인하고, 본문 전체를 44 LOC(diff 청크 50줄)로 통일함.
2. **"결론에서 NodeBB와 Element-Web의 동일 underrepresentation 묶기" 해결**:
   - NodeBB는 "명시적 요구조건(Explicit Requirement)의 오라클 검증 누락"으로, Element-Web은 "Mock 단위 검증과 추론된 영속 상태 조건(Inferred Requirement)의 범위 경계"로 결론 절(Section 8)에서 명확히 분리함.
3. **"Section 7.1의 'often truncate' 빈도 일반화" 해결**:
   - 4개 정성 사례를 근거로 벤치마크 전반에 빈번히 나타난다는 주장을 배제하고, "정성 사례에서 관찰된 평가 하네스의 국소적 검증 경향"으로 수위를 조절함.
4. **"Figure 1의 FINERACT 예시 출처 투명화" 해결**:
   - 단일 Jira 티켓의 직접 인용이 아닌 FINERACT-753과 2338의 비즈니스 로직을 요약한 예시적 합성(Illustrative Synthesis)임을 그림 상단과 본문에 명시함.
5. **"다수 연구자 수작업 분류 및 공동 판정 기록 부재" 해결 (P0-1)**:
   - 미수행된 다자 평가를 사실로 서술하지 않고, 1인 주연구자의 배치 주석 및 자동화 오프셋 검증 스크립트(`validate_*.py`) 절차로 정직하게 기술함.
   - Section 6.1에 다자 일치도 통계 부재를 명시적 한계로 고백하여 학술적 정직성을 확보함.
6. **"NodeBB #0030의 분석된 F2P 테스트 패치 단언 범위와 전체 런타임 하네스 일반화 분리" 해결 (4차 심사)**:
   - 분석된 F2P 테스트 패치(`test/messaging.js:L103-121`)에 마이그레이션 직접 단언문이 0건이라는 실측 사실과, 전체 벤치마크 런타임 하네스가 마이그레이션을 탐지하지 못한다는 일반화 주장을 엄밀히 구분하여 Abstract, Intro, Table 6, Sec 5.3, Conclusion 전반의 서술 수위를 정적 테스트 패치 단언 범위로 한정함.
7. **"Figure 1의 통계적 공기 표현 교정" 해결 (4차 심사)**:
   - 'Requirements co-occur independently'를 Section 5.1의 통계적 해석과 일치시켜 'Near-zero observed association'으로 수정함.
8. **"Section 7.1의 E1 매칭 방식 엄밀 표기" 해결 (4차 심사)**:
   - 네이티브 태그 및 파일 수의 정확 매칭($|Files(t_i)| = |Files(t_j)|$)과 churn의 허용 오차 윈도우 매칭($|LOC(t_i) - LOC(t_j)| \le \max(3, 30\% \times \max(LOC_i, LOC_j))$)을 엄밀히 분리 표기함.
9. **"Production Gap 원인 확정 표현 교정" 해결 (4차 심사)**:
   - Production Gap의 원인이 입증되었다는 식의 단정적 표현을 배제하고, 잠재적 평가·운영 불일치(potential evaluation-to-production mismatch)에 대한 구성 타당도(Construct Validity) 분석으로 수위를 조절함.

---

## 5. 실제 수행 기록을 확인하지 못한 항목 (Unverified Items Report)

원고의 학술적 신뢰성을 위해, 연구 수행 기록상 확인되지 않은 다음 사항들을 명시적으로 보고하며 본문에서 전면 배제하였음을 확인한다:

1. **다수 연구자의 독립 이중 평가 및 상호 일치도(IRR) 통계**:
   - 연구 기록상 2인 이상의 독립적인 병렬 블라인드 코딩이나 위원회 공동 판정 회의록은 존재하지 않음.
   - 과거 한때 언급되었던 Cohen's $\kappa=0.9100$은 근거 데이터가 확인되지 않아 철회되었으며, 이번 원고에서도 일체 언급하지 않음.
2. **미실행 태스크에 대한 동적 솔버 실행 및 통과 로그**:
   - `report.json`, `run_instance.log`, `benchmark_score=1.0` 등 가상의 벤치마크 실행 산출물은 존재하지 않음.
   - 따라서 본 논문의 NodeBB, Element-Web 분석은 동적 실행 결과가 아니라 **"제공된 F2P 테스트 코드 및 정답 diff의 정적 단언문 범위 분석(Static Test Oracle Assertion Scope)"**으로 엄격히 한정됨.
3. **Ablated 패치(마이그레이션 누락 패치)의 실제 벤치마크 환경 동적 채점 결과**:
   - 11개 수정 파일만 반영하고 `chat_allow_list.js`를 제외한 패치가 실제 벤치마크 도커 컨테이너에서 몇 점을 받는지 동적으로 채점한 기록은 없음.
   - 따라서 "마이그레이션을 생략해도 테스트를 100% 통과한다"는 식의 동적 과장 주장을 전면 배제하고, "제공된 `test/messaging.js`에는 마이그레이션을 검증하는 단언문이 0건이므로 오라클이 이를 평가할 수 없다"는 정적 오라클 한계로 엄밀히 한정함.

---

## 6. 검증의 범위: 자동화 계산 무결성 vs. 학술적 논증 타당성

### 1) 자동화 무결성 검증 (Automated Integrity Verification) — PASS
- `python Paper/v0.4/scripts/10_verify_gate4.py` 실행: **PASS (0 Failures, Exit Code 0)**
  - 본문 핵심 모수(Fineract 2,925, AI 944, Pro 731, Poly 165, EVO 48, 매칭쌍 1,177 등) 전수 일치 확인
  - Table 2~6 전 행·전 열 CSV 실측치 1:1 일치 확인
  - 금지 어휘(과장 인과, 가상 실행 주장 등 14개 어휘) 0건 확인
  - 필수 보정 문구 전수 반영 확인
- `python Paper/v0.4/scripts/09_verify_gate3.py` 실행: **PASS (0 Failures, Exit Code 0)**
  - 18개 기준 3대 패밀리 층화 통계 및 $\phi$ 공기 행렬 재계산 100% 일치 확인
  - Fineract 16대 의존관계 Jira JSON 바이트 단위 일치 확인

### 2) 학술적 의미 및 구성 타당도의 경계 (Academic Interpretive Scope)
- 자동화 검증 스크립트의 `PASS` 결과는 **데이터의 계산적 정확성, 파일 해시 일치, 바이트 오프셋 정합성**을 보증하는 기술적 검증입니다.
- 이는 논문이 담고 있는 모든 정성적 해석, 아키텍처적 인과 논증, 일반화 범위의 학술적 타당성이 "완벽히 증명"되었음을 의미하는 것은 아닙니다.
- 본 연구의 학술적 주장은 1인 주연구자 주석의 한계, Apache Fineract 코어뱅킹의 도메인 특수성, 정적 테스트 코드 단언문 분석의 범위라는 명확한 학술적 제약(Section 6) 하에서 해석되어야 합니다.
- 따라서 본 연구는 자동화 검증을 통해 실측 증거와의 엄밀한 일관성을 확보하고, 학술적 주장은 그 증거가 허용하는 경계 내에서 절제되고 정직하게 논증을 전개합니다.
