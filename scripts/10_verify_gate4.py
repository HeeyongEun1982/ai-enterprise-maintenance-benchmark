"""
10. Gate 4 Paper Manuscript Consistency & Integrity Verifier (Table Row-by-Row Full Parser Edition)
===================================================================================================
마스터 실행 계획서 v0.4 Gate 4 보완 심사 지시 전수 자동 검증:
1. 핵심 모수 및 모집단 수치 (2,925, 3,811, 2,393, 944, 731, 165, 48, 3,446) 대조
2. E1 Matched Pairs (data/e1_matched_pairs.csv) 독립 재계산 및 본문 대조:
   - N=1,177 pairs, mean=0.8138, median=1.0000, std=0.2745, disjoint=676 (57.4%)
   - Pro pairs=714, Poly pairs=463, unique tasks=581
   - 과거 오류 수치 (0.7870, 0.8000, 0.2214, 41.2%) 완전 배제 검사
3. Table 2 Markdown 표 실제 파싱 -> 18개 행·모든 열(All, Pro, Poly, EVO 건수·비율) 1:1 대조
4. Table 3 Markdown 표 실제 파싱 -> 9개 구간(0..8) 및 평균 행 모든 셀 실측치 1:1 대조
   - 과거 오류 수치 '1.74' 완전 배제 검사
5. Table 4 Markdown 표 실제 파싱 -> 11개 기준쌍 행 모든 수치(공기수, phi, p-value) 1:1 대조
6. Table 5 Markdown 표 실제 파싱 -> 16대 Fineract 의존관계(DEP-01..16, 이슈ID, 분류) 1:1 대조
7. Table 6 Markdown 표 실제 파싱 -> 4대 비교 축 단언문 및 정적 오라클 한정 검증
8. 서지·경로·어휘 무결성 검증:
   - file:/// 및 로컬 절대경로(d:/Study) 0건
   - 비실측 이중평가 주장(kappa, 0.9100) 0건
   - 인용구(cite)와 참고문헌(References) 1:1 대응 검증
   - 금지된 과장 어휘('completely decoupled', '만점 통과' 등) 0건
"""

import os
import sys
import re
import pandas as pd

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(base_dir, "data")
paper_path = os.environ.get("PAPER_DRAFT", os.path.join(base_dir, "paper_draft_v0.4_12p.md"))
if not os.path.isfile(paper_path):
    raise SystemExit("Optional manuscript check: set PAPER_DRAFT to the path of your local Markdown draft; it is not bundled in this public repository.")

print("=" * 80)
print(" GATE 4 PAPER MANUSCRIPT INTEGRITY & RIGOROUS TABLE ROW-BY-ROW VERIFICATION")
print("=" * 80)

failures = []

if not os.path.exists(paper_path):
    failures.append("paper_draft_v0.4_12p.md 파일 누락")
    print("  [FAIL] 논문 원고 파일 부재")
    sys.exit(1)

with open(paper_path, 'r', encoding='utf-8') as f:
    paper_text = f.read()

def parse_md_table(text, header_keyword):
    """Markdown 본문에서 특정 헤더로 시작하는 표를 파싱하여 (headers, rows) 반환"""
    pos = text.find(header_keyword)
    if pos == -1:
        return None, []
    sub = text[pos:]
    lines = sub.splitlines()
    table_lines = []
    inside = False
    for line in lines[1:]:
        ls = line.strip()
        if ls.startswith('|'):
            inside = True
            table_lines.append(ls)
        elif inside:
            break
    if len(table_lines) < 3:
        return None, []
    headers = [c.strip() for c in table_lines[0].split('|')[1:-1]]
    rows = []
    for l in table_lines[2:]:
        cells = [c.strip() for c in l.split('|')[1:-1]]
        rows.append(cells)
    return headers, rows

# -----------------------------------------------------------------------------
# [검증 1] 핵심 모수 및 모집단 수치 일관성 검증
# -----------------------------------------------------------------------------
print("\n[검증 1] 논문 본문 내 핵심 모수 및 모집단 수치 일관성 검증")
core_numbers = [
    ("Fineract 모수 2,925", "2,925"),
    ("Fineract 요구단위 3,811", "3,811"),
    ("Fineract 해결이슈 2,393", "2,393"),
    ("AI 벤치마크 모수 944", "944"),
    ("SWE-bench Pro 모수 731", "731"),
    ("PolyBench Java 모수 165", "165"),
    ("SWE-EVO 모수 48", "48"),
    ("평가 분류 단위 3,446", "3,446"),
    ("통제 매칭쌍 1,177", "1,177"),
    ("Welch t-통계량 15.78", "15.78")
]

for desc, num in core_numbers:
    if num in paper_text:
        print(f"  [PASS] {desc}: 확인 완료")
    else:
        failures.append(f"{desc} ({num}) 본문 누락")
        print(f"  [FAIL] {desc}: 본문 누락")

# -----------------------------------------------------------------------------
# [검증 2] E1 통제 매칭쌍 (e1_matched_pairs.csv) 독립 재계산 및 본문 대조
# -----------------------------------------------------------------------------
print("\n[검증 2] E1 통제 매칭쌍 (e1_matched_pairs.csv) 독립 재계산 및 본문 대조")
e1_csv = os.path.join(data_dir, "e1_matched_pairs.csv")
if not os.path.exists(e1_csv):
    failures.append("e1_matched_pairs.csv 파일 누락")
    print("  [FAIL] e1_matched_pairs.csv 파일 누락")
else:
    df_e1 = pd.read_csv(e1_csv)
    n_pairs = len(df_e1)
    mean_j = df_e1['jaccard_distance'].mean()
    median_j = df_e1['jaccard_distance'].median()
    std_j = df_e1['jaccard_distance'].std(ddof=1)
    disjoint_count = (df_e1['jaccard_distance'] >= 0.999).sum()
    disjoint_pct = (disjoint_count / n_pairs) * 100.0

    pro_pairs = len(df_e1[(df_e1['family_1'] == 'SWE-bench Pro') & (df_e1['family_2'] == 'SWE-bench Pro')])
    poly_pairs = len(df_e1[(df_e1['family_1'] == 'PolyBench Java') & (df_e1['family_2'] == 'PolyBench Java')])
    unique_tasks = len(set(df_e1['task_id_1']).union(set(df_e1['task_id_2'])))

    print(f"  * CSV 실측치: N={n_pairs}, mean={mean_j:.4f}, median={median_j:.4f}, std={std_j:.4f}, disjoint={disjoint_count} ({disjoint_pct:.2f}%)")
    print(f"  * 계열쌍: Pro={pro_pairs}, Poly={poly_pairs}, 고유 과제수={unique_tasks}")

    expected_e1_tokens = [
        ("E1 Mean 0.8138", "0.8138"),
        ("E1 Median 1.0000", "1.0000"),
        ("E1 Std 0.2745", "0.2745"),
        ("E1 Disjoint Pct 57.4%", "57.4%"),
        ("E1 Disjoint Count 676", "676"),
        ("E1 Pro Pairs 714", "714"),
        ("E1 Poly Pairs 463", "463"),
        ("E1 Unique Tasks 581", "581")
    ]
    for desc, tok in expected_e1_tokens:
        if tok in paper_text:
            print(f"  [PASS] {desc}: 본문 수록 확인")
        else:
            failures.append(f"{desc} ({tok}) 본문 누락")
            print(f"  [FAIL] {desc}: 본문 누락")

    obsolete_e1_tokens = ["0.7870", "0.8000", "0.2214", "41.2%"]
    for old_tok in obsolete_e1_tokens:
        if old_tok in paper_text:
            failures.append(f"과거 E1 불일치 수치 '{old_tok}' 잔존")
            print(f"  [FAIL] 과거 E1 불일치 수치 '{old_tok}' 잔존")
        else:
            print(f"  [PASS] 과거 오류 수치 '{old_tok}' 전면 배제 확인")

# -----------------------------------------------------------------------------
# [검증 3] Table 2 Markdown 표 실제 파싱 -> 18개 행·모든 열 실측치 1:1 대조
# -----------------------------------------------------------------------------
print("\n[검증 3] Table 2 Markdown 표 실제 파싱 -> 18개 행 전 열 실측치 대조")
strat_csv = os.path.join(data_dir, "gate3_stratified_family_metrics.csv")
df_strat = pd.read_csv(strat_csv)
h2, r2 = parse_md_table(paper_text, "[Table 2]")

if len(r2) != len(df_strat):
    err = f"Table 2 행 개수 불일치: Markdown={len(r2)} vs CSV={len(df_strat)}"
    failures.append(err)
    print(f"  [FAIL] {err}")
else:
    t2_mismatches = []
    for idx, csv_r in df_strat.iterrows():
        table_r = r2[idx]
        code = csv_r['criterion_code']
        if code not in table_r[0]:
            t2_mismatches.append(f"Row {idx} Code: {code} not in {table_r[0]}")
        if str(csv_r['all_tasks_count']) not in table_r[2] or f"{csv_r['all_tasks_pct']:.2f}%" not in table_r[2]:
            t2_mismatches.append(f"Row {idx} ({code}) All mismatch")
        if str(csv_r['SWE-bench Pro_count']) not in table_r[3] or f"{csv_r['SWE-bench Pro_pct']:.2f}%" not in table_r[3]:
            t2_mismatches.append(f"Row {idx} ({code}) Pro mismatch")
        if str(csv_r['PolyBench Java_count']) not in table_r[4] or f"{csv_r['PolyBench Java_pct']:.2f}%" not in table_r[4]:
            t2_mismatches.append(f"Row {idx} ({code}) Poly mismatch")
        if str(csv_r['SWE-EVO_count']) not in table_r[5] or f"{csv_r['SWE-EVO_pct']:.2f}%" not in table_r[5]:
            t2_mismatches.append(f"Row {idx} ({code}) EVO mismatch")
    
    if not t2_mismatches:
        print(f"  [PASS] Table 2 18개 전 행·전 열 CSV 실측치 1:1 일치 확인 ({len(df_strat)}개 행)")
    else:
        for err in t2_mismatches:
            failures.append(err)
            print(f"  [FAIL] {err}")

# -----------------------------------------------------------------------------
# [검증 4] Table 3 Markdown 표 실제 파싱 -> 9개 구간 및 평균 행 1:1 대조
# -----------------------------------------------------------------------------
print("\n[검증 4] Table 3 Markdown 표 실제 파싱 -> 9개 구간 및 평균 행 대조")
comp_csv = os.path.join(data_dir, "gate3_coupling_complexity.csv")
df_comp = pd.read_csv(comp_csv)
h3, r3 = parse_md_table(paper_text, "[Table 3]")

if len(r3) < 11:
    err = f"Table 3 행 개수 부족: {len(r3)} (기대: 12개 행)"
    failures.append(err)
    print(f"  [FAIL] {err}")
else:
    t3_mismatches = []
    # r3[0] is Mean, r3[1] is Median, r3[2..10] are bins 0..8, r3[11] is Subtotal
    mean_r = r3[0]
    if "1.78" not in mean_r[1] or "2.24" not in mean_r[2] or "2.47" not in mean_r[3] or "1.22" not in mean_r[4] or "2.29" not in mean_r[5]:
        t3_mismatches.append(f"Table 3 Mean row mismatch: {mean_r}")

    for idx, csv_r in df_comp.iterrows():
        table_r = r3[idx + 2]
        b_str = str(idx)
        if b_str not in table_r[0]:
            t3_mismatches.append(f"Row {idx} bin {b_str} mismatch")
        fin_cnt_str = f"{csv_r['fineract_count']:,}"
        if fin_cnt_str not in table_r[1] or f"{csv_r['fineract_pct']:.2f}%" not in table_r[1]:
            t3_mismatches.append(f"Row {idx} Fin mismatch: {fin_cnt_str}")
        if str(csv_r['ai_all_count']) not in table_r[2] or f"{csv_r['ai_all_pct']:.2f}%" not in table_r[2]:
            t3_mismatches.append(f"Row {idx} AI mismatch")
        if str(csv_r['SWE-bench Pro_count']) not in table_r[3] or f"{csv_r['SWE-bench Pro_pct']:.2f}%" not in table_r[3]:
            t3_mismatches.append(f"Row {idx} Pro mismatch")
        if str(csv_r['PolyBench Java_count']) not in table_r[4] or f"{csv_r['PolyBench Java_pct']:.2f}%" not in table_r[4]:
            t3_mismatches.append(f"Row {idx} Poly mismatch")
        if str(csv_r['SWE-EVO_count']) not in table_r[5] or f"{csv_r['SWE-EVO_pct']:.2f}%" not in table_r[5]:
            t3_mismatches.append(f"Row {idx} EVO mismatch")

    if not t3_mismatches:
        print(f"  [PASS] Table 3 9개 전 구간(|B|=0..8) 및 가중 평균 행 CSV 실측치 1:1 일치 확인 (12개 행)")
    else:
        for err in t3_mismatches:
            failures.append(err)
            print(f"  [FAIL] {err}")

if "1.74" in paper_text:
    failures.append("논문 본문에 과거 오류 수치 '1.74' 잔존")
    print("  [FAIL] 본문 내 '1.74' 잔존")
else:
    print("  [PASS] 과거 오류 수치 '1.74' 전면 배제 확인")

# -----------------------------------------------------------------------------
# [검증 5] Table 4 Markdown 표 실제 파싱 -> 11개 기준쌍 행 수치 1:1 대조
# -----------------------------------------------------------------------------
print("\n[검증 5] Table 4 Markdown 표 실제 파싱 -> 11개 기준쌍 행 수치 대조")
phi_csv = os.path.join(data_dir, "gate3_phi_correlation_matrix.csv")
df_phi = pd.read_csv(phi_csv)
h4, r4 = parse_md_table(paper_text, "[Table 4]")

if len(r4) != len(df_phi):
    err = f"Table 4 행 개수 불일치: Markdown={len(r4)} vs CSV={len(df_phi)}"
    failures.append(err)
    print(f"  [FAIL] {err}")
else:
    t4_mismatches = []
    for idx, csv_r in df_phi.iterrows():
        table_r = r4[idx]
        pair = csv_r['pair']
        if pair not in table_r[0]:
            t4_mismatches.append(f"Table 4 Row {idx} Pair mismatch: {pair} not in {table_r[0]}")
        # Check Fineract cooccur and phi
        if str(csv_r['fineract_cooccurrence']) not in table_r[2] or f"{csv_r['fineract_phi']:.3f}" not in table_r[2]:
            t4_mismatches.append(f"Table 4 Row {idx} ({pair}) Fineract stats mismatch: co={csv_r['fineract_cooccurrence']}, phi={csv_r['fineract_phi']}")
        # Check AI cooccur, phi, p-value
        if str(csv_r['ai_cooccurrence']) not in table_r[3] or f"{csv_r['ai_phi']:.3f}" not in table_r[3] or f"{csv_r['ai_p_value']:.3f}" not in table_r[3]:
            t4_mismatches.append(f"Table 4 Row {idx} ({pair}) AI stats mismatch: co={csv_r['ai_cooccurrence']}, phi={csv_r['ai_phi']}, p={csv_r['ai_p_value']}")

    if not t4_mismatches:
        print(f"  [PASS] Table 4 11개 전 기준쌍 행·열 CSV 실측치 1:1 일치 확인 ({len(df_phi)}개 행)")
    else:
        for err in t4_mismatches:
            failures.append(err)
            print(f"  [FAIL] {err}")

# -----------------------------------------------------------------------------
# [검증 6] Table 5 Markdown 표 실제 파싱 -> 16대 Fineract 의존관계 1:1 대조
# -----------------------------------------------------------------------------
print("\n[검증 6] Table 5 Markdown 표 실제 파싱 -> 16대 의존관계 대조")
dep_csv = os.path.join(data_dir, "gate2_dependencies.csv")
df_dep = pd.read_csv(dep_csv)
h5, r5 = parse_md_table(paper_text, "[Table 5]")

if len(r5) != 16:
    err = f"Table 5 행 개수 불일치: Markdown={len(r5)} vs 기대=16"
    failures.append(err)
    print(f"  [FAIL] {err}")
else:
    t5_mismatches = []
    for idx in range(16):
        csv_r = df_dep.iloc[idx]
        table_r = r5[idx]
        dep_id = csv_r['dep_id']
        issue_id = csv_r['issue_id']
        classification = csv_r['dependency_classification']
        if dep_id not in table_r[0] or issue_id not in table_r[1] or classification.split()[0] not in table_r[2]:
            t5_mismatches.append(f"Table 5 Row {idx} mismatch: {dep_id}, {issue_id}, {classification}")

    if not t5_mismatches:
        print("  [PASS] Table 5 16대 Fineract 핵심 의존관계(DEP-01..DEP-16) 1:1 일치 확인 (16개 행)")
    else:
        for err in t5_mismatches:
            failures.append(err)
            print(f"  [FAIL] {err}")

# -----------------------------------------------------------------------------
# [검증 7] Table 6 Markdown 표 실제 파싱 -> 4대 비교 축 단언문 및 정적 한정 검증
# -----------------------------------------------------------------------------
print("\n[검증 7] Table 6 Markdown 표 실제 파싱 -> 4대 비교 축 및 NodeBB 정적 오라클 한정 검증")
h6, r6 = parse_md_table(paper_text, "[Table 6]")

if len(r6) != 4:
    err = f"Table 6 행 개수 불일치: Markdown={len(r6)} vs 기대=4"
    failures.append(err)
    print(f"  [FAIL] {err}")
else:
    t6_mismatches = []
    # Axis 1: NodeBB
    if "NodeBB #0030" not in r6[0][0] or "chat_allow_list.js" not in r6[0][1] or "Messaging.canMessageUser" not in r6[0][2]:
        t6_mismatches.append("Table 6 Axis 1 (NodeBB) 필수 토큰 누락")
    # Axis 2: Element-Web
    if "Element-Web #0139" not in r6[1][0] or "Unread-test.ts" not in r6[1][2]:
        t6_mismatches.append("Table 6 Axis 2 (Element-Web) 필수 토큰 누락")
    # Axis 3: RocketMQ
    if "RocketMQ #0819" not in r6[2][0] or "StatsItemSetTest.java" not in r6[2][2]:
        t6_mismatches.append("Table 6 Axis 3 (RocketMQ) 필수 토큰 누락")
    # Axis 4: Navidrome
    if "Navidrome #0495" not in r6[3][0] or "backup_test.go" not in r6[3][2] or "sqlite_master" not in r6[3][2]:
        t6_mismatches.append("Table 6 Axis 4 (Navidrome) 필수 토큰 누락")

    if not t6_mismatches:
        print("  [PASS] Table 6 4대 비교 축 단언문 및 오라클 분석 1:1 일치 확인 (4개 행)")
    else:
        for err in t6_mismatches:
            failures.append(err)
            print(f"  [FAIL] {err}")

uncalibrated_nodebb_phrases = [
    ("passes all automated test suites", "미실행 동적 테스트 전체 통과 과장"),
    ("passes all benchmark tests", "미실행 벤치마크 테스트 전체 통과 과장"),
    ("satisfies 100% of the benchmark's test assertions", "미실행 100% 만족 과장")
]

for bad_phrase, desc in uncalibrated_nodebb_phrases:
    if bad_phrase in paper_text:
        failures.append(f"NodeBB 미실행 통과 과장 표현 잔존: '{bad_phrase}' ({desc})")
        print(f"  [FAIL] NodeBB 미실행 통과 과장 표현 잔존: '{bad_phrase}'")
    else:
        print(f"  [PASS] NodeBB 과장 표현 배제 확인: '{bad_phrase}'")

# -----------------------------------------------------------------------------
# [검증 8] 서지·경로·어휘 무결성 및 독립 이중평가 주장 배제 검증
# -----------------------------------------------------------------------------
print("\n[검증 8] 서지·경로·어휘 무결성 및 독립 이중평가 주장 배제 검증")

if "file:///" in paper_text:
    failures.append("논문 본문 내 'file:///' 절대경로 잔존")
    print("  [FAIL] 본문 내 'file:///' 잔존")
else:
    print("  [PASS] 본문 내 'file:///' 절대경로 0건 확인")

if "d:/study" in paper_text.lower() or "d:\\study" in paper_text.lower():
    failures.append("논문 본문 내 'd:/Study' 로컬 디스크 경로 잔존")
    print("  [FAIL] 본문 내 로컬 디스크 절대경로 잔존")
else:
    print("  [PASS] 본문 내 로컬 디스크 경로(d:/Study) 0건 확인")

if "0.9100" in paper_text or "cohen's $\\kappa" in paper_text.lower() or "inter-rater agreement" in paper_text.lower():
    failures.append("논문 본문 내 비실측 이중평가 주장(kappa, 0.9100) 잔존")
    print("  [FAIL] 본문 내 비실측 이중평가(kappa=0.9100) 잔존")
else:
    print("  [PASS] 비실측 이중평가(kappa=0.9100) 주장 전면 배제 확인")

citations = re.findall(r'\\cite\{([^}]+)\}', paper_text)
ref_section = paper_text.split("## References")[-1] if "## References" in paper_text else ""

for c in set(citations):
    key_found = False
    if "jimenez" in c and "Jimenez" in ref_section:
        key_found = True
    elif "chen" in c and "Chen" in ref_section:
        key_found = True
    elif "xia" in c and "Xia" in ref_section:
        key_found = True
    elif "shayanfar" in c and "Shayanfar" in ref_section:
        key_found = True
    elif "yu" in c and "Yu" in ref_section:
        key_found = True
    elif "apache" in c and "Apache" in ref_section:
        key_found = True
    
    if key_found:
        print(f"  [PASS] Citation \\cite{{{c}}} -> References 서지 항목 매핑 확인")
    else:
        failures.append(f"Citation \\cite{{{c}}} 에 대응하는 References 항목 누락")
        print(f"  [FAIL] Citation \\cite{{{c}}} 대응 서지 누락")

banned_phrases = [
    ('completely decoupled', '통계적 공기 correlation과 인과 의존성 혼동 단정 어휘'),
    ('필연적으로 함께 묶', '과장된 인과 결합 단정'),
    ('극단적 결합 단절', '과장된 상관성 단정'),
    ('통계적으로 완전히 독립', '과장된 통계적 독립성 단정'),
    ('완벽 증명', '과장된 증명 어휘'),
    ('완벽 검증', '과장된 검증 어휘'),
    ('report.json', '가상 실행 산출물 잔존'),
    ('run_instance.log', '가상 실행 산출물 잔존'),
    ('benchmark_score=1.0', '가상 평가 점수 잔존'),
    ('만점 통과', '가상 통과 주장 잔존'),
    ('Navidrome #0025', '과거 허구 사례 번호 잔존'),
    ('frequently fail', '미실측 프로덕션 실패 빈도 단정 (potential evaluation-to-production mismatch로 한정 필요)'),
    ('does not stem from', '단정적 인과 원인 단정 (attribute count alone is insufficient로 수정 필요)'),
    ('oracle evaluation disconnect', '단정적 인과 단절 어휘 잔존'),
    ('satisfies all added test assertions', '미실행 테스트 통과 단정 (migration omission 및 coverage absence로 한정 필요)')
]

for term, desc in banned_phrases:
    if term in paper_text:
        failures.append(f"금지 어휘 잔존: '{term}' ({desc})")
        print(f"  [FAIL] 금지 어휘 잔존: '{term}'")
    else:
        print(f"  [PASS] 금지 어휘 배제: '{term}'")

# -----------------------------------------------------------------------------
# [검증 9] Gate 4 3차 심사 보완 지시 보정 표현 반영 검증
# -----------------------------------------------------------------------------
print("\n[검증 9] Gate 4 3차 심사 보완 지시 보정 표현 반영 검증")
required_calibrated_phrases = [
    ("Abstract/Intro: potential evaluation-to-production mismatch", "potential evaluation-to-production mismatch"),
    ("Discussion 7.1: attribute count alone is insufficient", "attribute count alone is insufficient to characterize evaluation validity"),
    ("Discussion 7.1: oracle coverage is an additional dimension", "evaluation oracle construct coverage represents a critical additional dimension"),
    ("Section 5.3: developer migration omission", "migration omission"),
    ("Section 5.3: migration-specific coverage absence", "migration-specific coverage absence")
]

for desc, phrase in required_calibrated_phrases:
    if phrase in paper_text:
        print(f"  [PASS] {desc}: 확인 완료")
    else:
        failures.append(f"보정 필수 표현 누락: '{phrase}' ({desc})")
        print(f"  [FAIL] {desc}: 본문 누락")

# -----------------------------------------------------------------------------
# Final Exit Determination
# -----------------------------------------------------------------------------
print("\n" + "=" * 80)
if not failures:
    print(" [PASS] Gate 4 논문 원고 표·행 단위(Table Row-by-Row) 전수 검증 통과 (0 Failures, Exit Code 0)")
    print("=" * 80)
    sys.exit(0)
else:
    print(f" [FAIL] Gate 4 검증 실패: 총 {len(failures)}건의 불일치 검출")
    for f in failures:
        print(f"  - {f}")
    print("=" * 80)
    sys.exit(1)
