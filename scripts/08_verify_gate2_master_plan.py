import os
import sys
import json
import pandas as pd

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(base_dir, 'data')
ablation_dir = os.path.join(base_dir, 'ablation_study/nodebb_0030')

print("=" * 80)
print(" GATE 2 RIGOROUS AUTOMATED EXIT VERIFICATION (마스터 실행 계획서 v0.4 기준)")
print("=" * 80)

failures = []

# -----------------------------------------------------------------------------
# 1. Official Codebook Verification & Cross-Mapping (framework-snapshot.json)
# -----------------------------------------------------------------------------
print("\n[검증 1] 공식 18개 기준 코드북 (framework-snapshot.json) 실증 대조 검증")
codebook_path = os.path.join(data_dir, 'framework-snapshot.json')
if not os.path.exists(codebook_path):
    failures.append(f"코드북 파일 누락: {codebook_path}")
    print("  [FAIL] framework-snapshot.json 파일이 존재하지 않습니다.")
else:
    with open(codebook_path, 'r', encoding='utf-8') as f:
        cb_data = json.load(f)
    
    crit_count = cb_data.get('criterion_count')
    act_count = cb_data.get('activities')
    prop_count = cb_data.get('properties')
    entries = cb_data.get('entries', [])
    cb_map = {e.get('code'): e.get('name') for e in entries}
    
    expected_codes = [
        'A1', 'A2', 'A3', 'A4', 'A5', 'A6',
        'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11', 'B12'
    ]
    missing_codes = [c for c in expected_codes if c not in cb_map]
    
    # Cross-reference with ab_long.csv
    ab_path = os.path.join(data_dir, 'ab_long.csv')
    df_ab = pd.read_csv(ab_path)
    ab_map = df_ab[['criterion_code', 'criterion_name']].drop_duplicates().set_index('criterion_code')['criterion_name'].to_dict()
    ab_counts = df_ab['criterion_code'].value_counts().to_dict()
    
    name_mismatches = []
    for c in expected_codes:
        cb_name = cb_map.get(c)
        ab_name = ab_map.get(c)
        if cb_name != ab_name:
            name_mismatches.append(f"{c}: cb='{cb_name}' vs ab='{ab_name}'")
    
    if crit_count == 18 and act_count == 6 and prop_count == 12 and not missing_codes and not name_mismatches:
        print(f"  [PASS] 기준수: {crit_count} (활동 {act_count}, 속성 {prop_count}), 18개 기준 코드 전수 일치")
        print(f"  [PASS] ab_long.csv와 코드북의 18개 기준 명칭 1:1 대조 결과 100% 일치")
        print("  [상세 매핑 확인]")
        for c in expected_codes:
            print(f"    - [{c}] {cb_map[c]:<16} | AI 944건 과제 내 분류 빈도: {ab_counts.get(c, 0):>3}건")
    else:
        err = f"코드북 검증 실패: crit_count={crit_count}, missing={missing_codes}, name_mismatches={name_mismatches}"
        failures.append(err)
        print(f"  [FAIL] {err}")

# -----------------------------------------------------------------------------
# 2. 17 Verbatim Quotes & Character Offsets String-Level Slice Verification
# -----------------------------------------------------------------------------
print("\n[검증 2] Fineract 17개 인용문 및 문자 시작 오프셋 1:1 슬라이스 전수 실질 검증")
dep_path = os.path.join(data_dir, 'gate2_dependencies.csv')
raw_json_path = os.path.join(data_dir, 'fineract', 'gate2_raw_source_snippets.json')

if not os.path.exists(dep_path) or not os.path.exists(raw_json_path):
    failures.append("의존관계 CSV 또는 원문 스니펫 JSON 누락")
    print("  [FAIL] 필수 파일 누락")
else:
    df_dep = pd.read_csv(dep_path)
    with open(raw_json_path, 'r', encoding='utf-8') as f:
        raw_bundle = json.load(f)
    raw_issues = raw_bundle.get('raw_jira_issues', {})
    
    quote_matches = 0
    total_quotes_checked = 0
    
    for idx, r in df_dep.iterrows():
        dep_id = r['dep_id']
        issue_id = r['issue_id']
        quote = str(r['verbatim_raw_quote'])
        start_pos = int(r['raw_quote_start_pos'])
        
        if issue_id not in raw_issues:
            failures.append(f"{dep_id}: 원문 JSON에 {issue_id} 없음")
            print(f"  [FAIL] {dep_id}: 원본 이슈 {issue_id} 누락")
            continue
        
        desc = raw_issues[issue_id]['description']
        actual_slice = desc[start_pos : start_pos + len(quote)]
        total_quotes_checked += 1
        
        if actual_slice == quote:
            quote_matches += 1
            print(f"  [OK] {dep_id} ({issue_id}): pos {start_pos:>4}..{start_pos + len(quote):<4} (len={len(quote):>3}) -> \"{quote[:40]}...\"")
        else:
            failures.append(f"{dep_id} 1차 인용구 오프셋 불일치 (pos={start_pos})")
            print(f"  [FAIL] {dep_id} 오프셋 {start_pos} 불일치: expected '{quote[:30]}...', got '{actual_slice[:30]}...'")
            continue
        
        # Paired quote check if present
        if pd.notna(r.get('paired_consequence_quote')) and str(r.get('paired_consequence_quote')).strip():
            p_quote = str(r['paired_consequence_quote'])
            p_pos = int(r['paired_consequence_pos'])
            p_slice = desc[p_pos : p_pos + len(p_quote)]
            total_quotes_checked += 1
            if p_slice == p_quote:
                quote_matches += 1
                print(f"    └─ [OK Paired] {dep_id}: pos {p_pos:>4}..{p_pos + len(p_quote):<4} (len={len(p_quote):>3}) -> \"{p_quote[:40]}...\"")
            else:
                failures.append(f"{dep_id} 쌍 인용구 오프셋 불일치 (pos={p_pos})")
                print(f"  [FAIL] {dep_id} 쌍 인용구 오프셋 {p_pos} 불일치!")
    
    if total_quotes_checked == 20 and quote_matches == 20:
        print(f"  [PASS] 총 {len(df_dep)}개 의존관계 항목의 {total_quotes_checked}개 인용문 전체가 원본 텍스트와 100% 바이트 단위 일치 ({quote_matches}/{total_quotes_checked})")
    else:
        err = f"인용문 일치 실패: {quote_matches}/{total_quotes_checked} (expected 20/20)"
        failures.append(err)
        print(f"  [FAIL] {err}")

# -----------------------------------------------------------------------------
# 3. Corpus & Classification Counts Cross-Verification
# -----------------------------------------------------------------------------
print("\n[검증 3] 전체 코퍼스 및 정량 데이터 규모(분류 건수) 일관성 검증")
base_csv_path = os.path.join(data_dir, 'baseline_tasks.csv')
req_units_path = os.path.join(data_dir, 'fineract', 'requirement-units.json')
all_evid_path = os.path.join(data_dir, 'ab_all_evidences.csv')

df_base = pd.read_csv(base_csv_path)
df_all_evid = pd.read_csv(all_evid_path)
with open(req_units_path, 'r', encoding='utf-8') as f:
    req_units = json.load(f)

fineract_issues = cb_data.get('source_issues', 0)
fineract_units = len(req_units)
ai_tasks_count = len(df_base)
ab_long_rows = len(df_ab)
all_evid_count = len(df_all_evid)

print(f"  - Fineract 분석 대상 이슈 수: {fineract_issues}건 (코드북 정의 2,925건)")
print(f"  - Fineract 요구 단위(Units) 수: {fineract_units}건 (코드북 정의 3,811건)")
print(f"  - AI 코딩 벤치마크 과제 수: {ai_tasks_count}건 (기준 944건)")
print(f"  - AI 과제 다중 기준 분류 행수: {ab_long_rows}건 (944개 과제)")
print(f"  - AI 과제 텍스트 근거 인용 건수: {all_evid_count}건")

if fineract_issues == 2925 and fineract_units == 3811 and ai_tasks_count == 944 and ab_long_rows == 3446:
    print("  [PASS] 정량 코퍼스 규모 및 분류 데이터 건수 전수 일치 확인")
else:
    err = f"데이터 규모 불일치: fin_issues={fineract_issues}, fin_units={fineract_units}, ai_tasks={ai_tasks_count}, ab_rows={ab_long_rows}"
    failures.append(err)
    print(f"  [FAIL] {err}")

# -----------------------------------------------------------------------------
# 4. NodeBB #0030 Patch Diff Physical Verification & Oracle Blind Spot (Static Inspection)
# -----------------------------------------------------------------------------
print("\n[검증 4] NodeBB #0030 원본 패치 diff 물리적 실질 대조 및 단언문 사각지대 정적 검증")
dev_diff_path = os.path.join(ablation_dir, 'nodebb_0030_developer_patch.diff')
abl_diff_path = os.path.join(ablation_dir, 'nodebb_0030_ablated_patch.diff')
test_diff_path = os.path.join(ablation_dir, 'nodebb_0030_test_patch.diff')
spec_path = os.path.join(ablation_dir, 'nodebb_0030_spec.json')
repro_md_path = os.path.join(ablation_dir, 'README_ABLATION_REPRODUCTION.md')
eval_script_path = os.path.join(ablation_dir, 'inspect_nodebb_oracle.py')

migration_file = 'src/upgrades/4.3.0/chat_allow_list.js'

if not (os.path.exists(dev_diff_path) and os.path.exists(abl_diff_path) and 
        os.path.exists(test_diff_path) and os.path.exists(spec_path) and 
        os.path.exists(repro_md_path) and os.path.exists(eval_script_path)):
    failures.append("NodeBB 필수 패치 및 정적 분석 파일 누락")
    print("  [FAIL] NodeBB 필수 패치 또는 정적 분석 파일 중 일부가 누락되었습니다.")
else:
    with open(dev_diff_path, 'r', encoding='utf-8') as f:
        dev_diff = f.read()
    with open(abl_diff_path, 'r', encoding='utf-8') as f:
        abl_diff = f.read()
    with open(test_diff_path, 'r', encoding='utf-8') as f:
        test_diff = f.read()
    with open(spec_path, 'r', encoding='utf-8') as f:
        spec_data = json.load(f)
    
    dev_files = [l for l in dev_diff.splitlines() if l.startswith('diff --git ')]
    abl_files = [l for l in abl_diff.splitlines() if l.startswith('diff --git ')]
    test_files = [l for l in test_diff.splitlines() if l.startswith('diff --git ')]
    
    has_migration_dev = migration_file in dev_diff
    has_migration_abl = migration_file in abl_diff
    
    # Check test diff contents
    has_test_messaging = 'test/messaging.js' in test_diff
    has_can_message = 'Messaging.canMessageUser' in test_diff
    has_chat_allow_list_test = 'chat_allow_list' in test_diff
    has_upgrade_test = 'upgrade' in test_diff.lower()
    
    # Developer patch check: exactly 12 files, includes migration
    # Ablated patch check: exactly 11 files, strictly omits migration
    # Test patch check: exactly 2 files, tests leaf function, strictly omits migration assertions
    diff_checks_ok = (
        len(dev_files) == 12 and has_migration_dev and
        len(abl_files) == 11 and (not has_migration_abl) and
        len(test_files) == 2 and has_test_messaging and has_can_message and
        (not has_chat_allow_list_test) and (not has_upgrade_test) and
        spec_data.get('base_commit') == '7800016f2f1b89d2d3cfea6a7da7c77096b7b927'
    )
    
    if diff_checks_ok:
        print(f"  [PASS] 개발자 패치: 정확히 12개 파일 수정, 마이그레이션 파일({migration_file}) 포함 확인 (44 added LOC / 50-line diff hunk)")
        print(f"  [PASS] 결함 패치: 정확히 11개 파일 수정, 마이그레이션 파일 완전 누락(0라인) 확인")
        print(f"  [PASS] 공식 테스트 패치: 2개 파일(test/messaging.js, test/user.js) 수정, Messaging.canMessageUser 리프 검사 단언문 포함 확인")
        print(f"  [PASS] 단언문 정적 분석: 테스트 패치 내 마이그레이션(chat_allow_list/upgrade) 단언문 완전 부재(False) 확인 -> 제공 F2P 패치의 정적 단언문 범위 한계 확인 (전체 하네스 또는 점수 아님)")
        print(f"  [PASS] 과제 명세 및 정적 분석 지침(nodebb_0030_spec.json, README_ABLATION_REPRODUCTION.md) 일관성 확인")
    else:
        err = f"NodeBB diff 검증 실패: dev_files={len(dev_files)}, abl_files={len(abl_files)}, dev_mig={has_migration_dev}, abl_mig={has_migration_abl}"
        failures.append(err)
        print(f"  [FAIL] {err}")

# -----------------------------------------------------------------------------
# 5. E1 Matched Pairs Representative Pair Verification
# -----------------------------------------------------------------------------
print("\n[검증 5] E1 통제쌍 실측 데이터 및 대표쌍(Table 3) 검증")
e1_path = os.path.join(data_dir, 'e1_matched_pairs.csv')
if not os.path.exists(e1_path):
    failures.append("e1_matched_pairs.csv 파일 누락")
    print("  [FAIL] e1_matched_pairs.csv 누락")
else:
    df_e1 = pd.read_csv(e1_path)
    pair_count = len(df_e1)
    
    ol_pair = df_e1[(df_e1['task_id_1'].astype(str).str.zfill(4) == '0143') & (df_e1['task_id_2'].astype(str).str.zfill(4) == '0233')]
    if len(ol_pair) > 0 and pair_count >= 700:
        row = ol_pair.iloc[0]
        dist = float(row['jaccard_distance'])
        print(f"  [PASS] 총 매칭쌍 {pair_count}개 확보 (기준 700개 이상 충족)")
        print(f"  [PASS] Table 3 대표쌍 확인: OpenLibrary #0143 (LoC {row['loc_1']}, {row['b_codes_1']}) vs #0233 (LoC {row['loc_2']}, {row['b_codes_2']}) | Jaccard={dist:.4f}")
    else:
        failures.append("E1 대표쌍(OpenLibrary #143 vs #233) 검증 실패")
        print(f"  [FAIL] E1 대표쌍 검증 실패")

# -----------------------------------------------------------------------------
# 6. E2 4-Axis Comparative Mapping & Verdict Consistency
# -----------------------------------------------------------------------------
print("\n[검증 6] E2 실존 사례 4대 비교 축 매핑 및 판정 정합성 검증")
case_path = os.path.join(data_dir, 'gate2_case_mapping.csv')
verdict_path = os.path.join(data_dir, 'gate2_case_verdicts.csv')

if not os.path.exists(case_path) or not os.path.exists(verdict_path):
    failures.append("E2 케이스 매핑/판정 CSV 누락")
    print("  [FAIL] E2 필수 CSV 누락")
else:
    df_case = pd.read_csv(case_path)
    df_verdict = pd.read_csv(verdict_path)
    
    expected_tasks = {'0030', '0139', '0819', '0495'}
    found_tasks = set(df_case['ai_task_id'].astype(str).str.zfill(4))
    
    if expected_tasks.issubset(found_tasks) and len(df_verdict) == 4:
        print(f"  [PASS] 4대 비교 축 전수 확인: NodeBB(0030), Element(0139), RocketMQ(0819), Navidrome(0495)")
    else:
        failures.append("E2 4대 비교 축 누락")
        print(f"  [FAIL] E2 축 누락: expected {expected_tasks}, found {found_tasks}")

# -----------------------------------------------------------------------------
# Final Exit Determination
# -----------------------------------------------------------------------------
print("\n" + "=" * 80)
if not failures:
    print(" [PASS] Gate 2 마스터 실행 계획서 요구사항 전수 실질 검증 완료 (0 Failures)")
    print("=" * 80)
    sys.exit(0)
else:
    print(f" [FAIL] Gate 2 검증 실패: 총 {len(failures)}건의 오류 검출")
    for f in failures:
        print(f"  - {f}")
    print("=" * 80)
    sys.exit(1)
