# [NodeBB #0030 정적 코드 diff 및 테스트 오라클 단언문 분석]
## Qualitative Code Diff & Test Oracle Inspection Analysis: Construct Underrepresentation in SWE-bench Pro

* **대상 인스턴스 (Target Instance)**: `instance_NodeBB__NodeBB-a5afad27e52fd336163063ba40dcadc80233ae10-vd59a5728dfc977f44533186ace531248c2917516`
* **기준 저장소 및 커밋 (Base Commit)**: `NodeBB/NodeBB` @ `7800016f2f1b89d2d3cfea6a7da7c77096b7b927`
* **정적 분석 스크립트**: [`inspect_nodebb_oracle.py`](inspect_nodebb_oracle.py)

---

## 1. 분석 목적 및 배경 (Analytical Purpose)

* **핵심 질문**: 
  > *"과제 요구명세(Specification)에 명시된 필수 데이터 이행(DB Migration, $A_5$)과 불변성 보존($B_6$)을 완전히 누락한 결함 패치를 AI 모델이 제출했을 때, 기존 벤치마크 평가 오라클(Test Oracle)의 단언문은 이를 검증할 수 있는가?"*
* **비교 대상 패치 diff**:
  - 인간 개발자 정답 패치([`nodebb_0030_developer_patch.diff`](nodebb_0030_developer_patch.diff)): 총 12개 파일 수정, **비동기 DB 마이그레이션 배치 스크립트**(`src/upgrades/4.3.0/chat_allow_list.js`, 44 added LOC; 50-line diff hunk) 포함.
  - 결함 후보 패치([`nodebb_0030_ablated_patch.diff`](nodebb_0030_ablated_patch.diff)): `Messaging.canMessageUser` 리프 권한 검사 함수만 수정하고, **DB 마이그레이션 스크립트를 100% 누락 (0라인 생성, 총 11개 파일만 수정)**.
  - 공식 벤치마크 테스트 패치([`nodebb_0030_test_patch.diff`](nodebb_0030_test_patch.diff)): 총 2개 파일(`test/messaging.js`, `test/user.js`) 수정.

---

## 2. 코드 레벨 diff 구조 비교 (Patch Diff Structural Verification)

| 비교 항목 | 개발자 실제 정답 패치 | 결함 후보 모델 패치 | 차이점 및 오미션(Omission) |
| :--- | :---: | :---: | :--- |
| **수정 파일 수** | **12개 파일** | **11개 파일** | 1개 파일 누락 |
| **패치 구성** | 12개 파일 | 11개 파일 | 이행 파일 전체 누락 (수치상 LOC와 diff hunk는 구분) |
| **`src/upgrades/4.3.0/chat_allow_list.js`** | **포함 (44 added LOC; 50-line diff hunk)** | **완전 누락** | **핵심 DB 마이그레이션 파일 누락** |
| **리프 권한 검사 수정** | 포함 (`src/messaging/index.js` 등) | 포함 (`src/messaging/index.js` 등) | 실시간 API 분기는 동일 구현 |

---

## 3. 평가 오라클 단언문 정적 분석 (Test Oracle Scope Analysis)

공식 테스트 패치([`nodebb_0030_test_patch.diff`](nodebb_0030_test_patch.diff))의 F2P 단언문(`test/messaging.js:L103-121`) 코드는 다음과 같이 작성되어 있습니다:

```javascript
// test/messaging.js:L103-121
it('should respect allow/deny list when sending chat messages', async () => {
    // 1. 테스트 실행 시점에 신규 임시 사용자 3명을 생성
    const uid1 = await User.create({ username: 'allowdeny1', password: 'barbar' });
    const uid2 = await User.create({ username: 'allowdeny2', password: 'bazbaz' });
    const uid3 = await User.create({ username: 'allowdeny3', password: 'bazbaz' });
    await Messaging.canMessageUser(uid1, uid2);

    // 2. 신규 사용자에게 직접 API를 통해 chatAllowList 설정을 주입함
    await User.setSetting(uid1, 'chatAllowList', JSON.stringify([uid3]));
    await assert.rejects(Messaging.canMessageUser(uid2, uid1), { message: '[[error:chat-restricted]]' });

    // 3. chatDenyList 설정을 직접 주입함
    await User.setSetting(uid2, 'chatDenyList', JSON.stringify([uid1]));
    await assert.rejects(Messaging.canMessageUser(uid1, uid2), { message: '[[error:chat-restricted]]' });
});
```

### 오라클의 구조적 한계 (Oracle Blind Spot)
1. **임시 Mock 사용자 한정 검증**:
   - 위 테스트는 매 실행마다 신규 사용자(`User.create`)를 생성한 뒤 메모리 상에서 `User.setSetting`으로 새 설정값을 직접 주입합니다.
   - 따라서 과거 버전 포럼에서 `restrictChat=1`을 사용하던 레거시 데이터베이스 상태가 존재하는 환경을 전혀 검증하지 않습니다.
2. **마이그레이션 단언문 부재 (Zero Assertions)**:
   - 테스트 스위트 전체(`test/messaging.js`, `test/user.js`)를 전수 검토한 결과, 업그레이드 스크립트(`src/upgrades/4.3.0/chat_allow_list.js`)를 호출하거나 데이터 일괄 이행 상태를 단언하는 코드가 전혀 존재하지 않습니다.
3. **단언문 검증 범위의 한계**:
   - 테스트 오라클은 리프 권한 판정 함수(`Messaging.canMessageUser`)만을 단언 대상으로 삼고 있어, 44라인의 핵심 데이터베이스 이행 스크립트가 완전히 누락되어도 단언문 레벨에서 이를 감지할 수 없는 구조적 사각지대를 가집니다.

---

## 4. 학술적 의의: 개념 구성체 과소대표 (Construct Underrepresentation)

본 정적 분석은 논문의 핵심 학술적 가설인 **평가 구성 타당성의 결핍(Construct Underrepresentation)**을 코드 레벨에서 명확히 실증합니다:
1. 분석한 **F2P 테스트 패치**에는 로컬 권한 판정 단언문이 있으나, 필수 데이터 이행과 기존 상태 불변식의 직접 단언문이 확인되지 않았습니다. 이는 전체 평가 하네스에서의 미검출을 입증하지 않습니다.
2. 본 사례는 **제공된 개발자 패치와 F2P 테스트 패치의 정적 비교**로 확인할 수 있는 단언문 범위 차이만 기술합니다. 전체 오라클의 성공·실패나 벤치마크 점수는 측정하지 않았습니다.


**Scope restriction:** The analysis inspects the provided F2P test patch statically. It does not run the complete benchmark harness or establish a scored pass/fail outcome. The migration file is 44 added lines (50-line unified diff hunk); these are different quantities.
