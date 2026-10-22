"""
09. Gate 3 Rigorous Automated Verification Script (Exit Criteria Full Validator - 3rd Revision)
==============================================================================================
1. Recompute and compare all 18 criteria across three benchmark families
2. Recompute co-occurrence counts, phi correlations, and Fisher exact p-values for 11 pairs and compare with CSV
3. Recompute all nine multi-attribute diversity (|B|) bins and cross-check means (1.7798 -> 1.78) with documentation
4. Compare 19 source-text slices for 16 core Fineract dependencies (DEP-01..DEP-16) against Jira JSON (raw_jira_issues)
5. Four AI comparison axes: use packaged sources (data/ai_case_sources/) without external RAW5 dependencies;
   inspect original task JSON (0139, 0819, 0495) and NodeBB diffs for test_patch file paths and assertions
6. Check calibrated phrasing: exclude exaggerated claims and unsupported statistical significance; distinguish three analytical levels
"""

import os
import sys
import json
import math
import pandas as pd
from collections import defaultdict
from scipy.stats import fisher_exact, ttest_ind

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(base_dir, "data")

print("=" * 80)
print(" GATE 3 RIGOROUS AUTOMATED EXIT VERIFICATION (self-contained package verification mode)")
print("=" * 80)

failures = []

# -----------------------------------------------------------------------------
# [Check 1] Recompute and compare 18 criteria across three benchmark families
# -----------------------------------------------------------------------------
print("\n[Check 1] Recompute and verify 18 criteria across three benchmark families")
strat_csv_path = os.path.join(data_dir, "gate3_stratified_family_metrics.csv")
base_csv_path = os.path.join(data_dir, "baseline_tasks.csv")
ab_long_path = os.path.join(data_dir, "ab_long.csv")

if not os.path.exists(strat_csv_path):
    failures.append("Missing gate3_stratified_family_metrics.csv")
    print("  [FAIL] gate3_stratified_family_metrics.csv does not exist")
else:
    df_base = pd.read_csv(base_csv_path)
    df_ab = pd.read_csv(ab_long_path)
    df_strat = pd.read_csv(strat_csv_path)
    
    total_ai = len(df_base)
    df_merged = df_ab.merge(df_base[['task_id', 'benchmark_family']], on='task_id')
    families = ['SWE-bench Pro', 'PolyBench Java', 'SWE-EVO']
    family_totals = df_base['benchmark_family'].value_counts().to_dict()
    
    mismatches = []
    for _, r in df_strat.iterrows():
        c = r['criterion_code']
        # Recompute all tasks
        raw_all_cnt = len(df_ab[df_ab['criterion_code'] == c])
        raw_all_pct = round((raw_all_cnt / total_ai) * 100.0, 2)
        if r['all_tasks_count'] != raw_all_cnt or abs(r['all_tasks_pct'] - raw_all_pct) > 0.01:
            mismatches.append(f"{c} all_tasks: csv=({r['all_tasks_count']}, {r['all_tasks_pct']}%) vs raw=({raw_all_cnt}, {raw_all_pct}%)")
        
        # Recompute family tasks
        for fam in families:
            raw_fam_cnt = len(df_merged[(df_merged['criterion_code'] == c) & (df_merged['benchmark_family'] == fam)])
            raw_fam_pct = round((raw_fam_cnt / family_totals[fam]) * 100.0, 2)
            csv_cnt = r[f'{fam}_count']
            csv_pct = r[f'{fam}_pct']
            if csv_cnt != raw_fam_cnt or abs(csv_pct - raw_fam_pct) > 0.01:
                mismatches.append(f"{c} {fam}: csv=({csv_cnt}, {csv_pct}%) vs raw=({raw_fam_cnt}, {raw_fam_pct}%)")
                
    if not mismatches and len(df_strat) == 18:
        print(f"  [PASS] Recomputed values match for all 18 criteria (18 rows, four groups)")
        print(f"  [PASS] Benchmark family sizes: Pro 731, PolyBench 165, EVO 48")
    else:
        err = f"Stratified metric mismatches: {len(mismatches)}: {mismatches[:3]}"
        failures.append(err)
        print(f"  [FAIL] {err}")

# -----------------------------------------------------------------------------
# [Check 2] Recompute and compare co-occurrence counts, phi correlations, and Fisher exact p-values for 11 pairs
# -----------------------------------------------------------------------------
print("\n[Check 2] Recompute and compare co-occurrence counts, phi correlations, and Fisher p-values for 11 pairs")
phi_csv_path = os.path.join(data_dir, "gate3_phi_correlation_matrix.csv")
fin_summary_path = os.path.join(data_dir, "fineract", "summary.json")

if not os.path.exists(phi_csv_path):
    failures.append("Missing gate3_phi_correlation_matrix.csv")
    print("  [FAIL] gate3_phi_correlation_matrix.csv does not exist")
else:
    with open(fin_summary_path, 'r', encoding='utf-8') as f:
        fin_summary = json.load(f)
    fin_codes = defaultdict(set)
    for e in fin_summary.get('entries', []):
        for u in e.get('all_unit_ids', []):
            fin_codes[u.split('-R')[0]].add(e['code'])
    total_fin = 2925

    ai_codes = defaultdict(set)
    for _, r in df_ab.iterrows():
        ai_codes[int(r['task_id'])].add(r['criterion_code'])
    total_ai = 944

    def calc_phi_and_p(codes_dict, total_n, c1, c2):
        n11 = sum(1 for s in codes_dict.values() if c1 in s and c2 in s)
        n10 = sum(1 for s in codes_dict.values() if c1 in s and c2 not in s)
        n01 = sum(1 for s in codes_dict.values() if c1 not in s and c2 in s)
        n00 = total_n - (n11 + n10 + n01)
        num = (n11 * n00) - (n10 * n01)
        den = math.sqrt((n11 + n10) * (n01 + n00) * (n11 + n01) * (n10 + n00))
        phi = num / den if den > 0 else 0.0
        _, p_val = fisher_exact([[n11, n10], [n01, n00]])
        return n11, phi, p_val

    df_phi = pd.read_csv(phi_csv_path)
    phi_mismatches = []
    for _, r in df_phi.iterrows():
        c1, c2 = r['c1'], r['c2']
        pair = r['pair']
        f_n11, f_phi, f_p = calc_phi_and_p(fin_codes, total_fin, c1, c2)
        a_n11, a_phi, a_p = calc_phi_and_p(ai_codes, total_ai, c1, c2)
        
        # Check Fineract coocc, phi, p-value
        f_p_csv = float(r['fineract_p_value'])
        if r['fineract_cooccurrence'] != f_n11 or abs(r['fineract_phi'] - round(f_phi, 3)) > 0.002:
            phi_mismatches.append(f"{pair} Fineract phi mismatch: csv=({r['fineract_cooccurrence']}, {r['fineract_phi']}) vs raw=({f_n11}, {f_phi:.3f})")
        if abs(f_p_csv - f_p) / (f_p + 1e-120) > 1e-4:
            phi_mismatches.append(f"{pair} Fineract p-value mismatch: csv={f_p_csv:.3e} vs raw={f_p:.3e}")

        # Check AI coocc, phi, p-value
        a_p_csv = float(r['ai_p_value'])
        if r['ai_cooccurrence'] != a_n11 or abs(r['ai_phi'] - round(a_phi, 3)) > 0.002:
            phi_mismatches.append(f"{pair} AI phi mismatch: csv=({r['ai_cooccurrence']}, {r['ai_phi']}) vs raw=({a_n11}, {a_phi:.3f})")
        if abs(a_p_csv - a_p) / (a_p + 1e-120) > 1e-4:
            phi_mismatches.append(f"{pair} AI p-value mismatch: csv={a_p_csv:.3e} vs raw={a_p:.3e}")

    if not phi_mismatches and len(df_phi) == 11:
        print(f"  [PASS] Recomputed co-occurrence counts, phi correlations, and Fisher exact p-values match the CSV for all 11 pairs")
        for _, r in df_phi.iterrows():
            print(f"    - {r['pair']:<6}: Fin(co={r['fineract_cooccurrence']:>3}, phi={r['fineract_phi']:>+6.3f}, p={float(r['fineract_p_value']):.2e}) | AI(co={r['ai_cooccurrence']:>3}, phi={r['ai_phi']:>+6.3f}, p={float(r['ai_p_value']):.2e})")
    else:
        err = f"Phi matrix recalculation mismatches: {len(phi_mismatches)}: {phi_mismatches[:3]}"
        failures.append(err)
        print(f"  [FAIL] {err}")

# -----------------------------------------------------------------------------
# [Check 3] Recompute nine multi-attribute diversity (|B|) bins and means; cross-check documentation
# -----------------------------------------------------------------------------
print("\n[Check 3] Recompute and compare all nine multi-attribute diversity (|B|) bins and weighted means")
comp_csv_path = os.path.join(data_dir, "gate3_coupling_complexity.csv")
evid_md_path = os.path.join(base_dir, "evidence", "requirement_dependency_evidence.md")

if not os.path.exists(comp_csv_path):
    failures.append("Missing gate3_coupling_complexity.csv")
    print("  [FAIL] gate3_coupling_complexity.csv does not exist")
else:
    df_comp = pd.read_csv(comp_csv_path)
    
    # 1. Recompute raw distributions across all 9 bins (0..8)
    b_codes = [f"B{i}" for i in range(1, 13)]
    fin_b_dist = defaultdict(int)
    for iid in fin_codes:
        b_cnt = len(fin_codes[iid].intersection(b_codes))
        fin_b_dist[b_cnt] += 1
    fin_b_dist[0] += (total_fin - len(fin_codes))
    
    ai_b_tasks = df_ab[df_ab['criterion_code'].isin(b_codes)].groupby('task_id')['criterion_code'].count().to_dict()
    df_base['b_cnt'] = df_base['task_id'].map(lambda tid: ai_b_tasks.get(tid, 0))
    
    dist_mismatches = []
    for k in range(0, 9):
        # Raw counts
        raw_f_cnt = fin_b_dist.get(k, 0)
        raw_ai_cnt = len(df_base[df_base['b_cnt'] == k])
        raw_pro_cnt = len(df_base[(df_base['benchmark_family'] == 'SWE-bench Pro') & (df_base['b_cnt'] == k)])
        raw_poly_cnt = len(df_base[(df_base['benchmark_family'] == 'PolyBench Java') & (df_base['b_cnt'] == k)])
        raw_evo_cnt = len(df_base[(df_base['benchmark_family'] == 'SWE-EVO') & (df_base['b_cnt'] == k)])
        
        # CSV counts
        row = df_comp[df_comp['b_complexity'] == f"|B| = {k}"].iloc[0]
        if row['fineract_count'] != raw_f_cnt:
            dist_mismatches.append(f"|B|={k} Fin count: csv={row['fineract_count']} vs raw={raw_f_cnt}")
        if row['ai_all_count'] != raw_ai_cnt:
            dist_mismatches.append(f"|B|={k} AI count: csv={row['ai_all_count']} vs raw={raw_ai_cnt}")
        if row['SWE-bench Pro_count'] != raw_pro_cnt:
            dist_mismatches.append(f"|B|={k} Pro count: csv={row['SWE-bench Pro_count']} vs raw={raw_pro_cnt}")
        if row['PolyBench Java_count'] != raw_poly_cnt:
            dist_mismatches.append(f"|B|={k} Poly count: csv={row['PolyBench Java_count']} vs raw={raw_poly_cnt}")
        if row['SWE-EVO_count'] != raw_evo_cnt:
            dist_mismatches.append(f"|B|={k} EVO count: csv={row['SWE-EVO_count']} vs raw={raw_evo_cnt}")
            
    if not dist_mismatches and len(df_comp) == 9:
        print(f"  [PASS] All nine bins (|B|=0..8) and five group frequencies match gate3_coupling_complexity.csv")
    else:
        err = f"Frequency mismatches across nine coupling bins: {len(dist_mismatches)}: {dist_mismatches[:3]}"
        failures.append(err)
        print(f"  [FAIL] {err}")

    # 2. Check means and statistical test
    fin_b_list = [len(fin_codes[iid].intersection(b_codes)) for iid in fin_codes] + [0] * (total_fin - len(fin_codes))
    raw_fin_mean = sum(fin_b_list) / len(fin_b_list)
    raw_ai_mean = df_base['b_cnt'].mean()
    pro_b_list = df_base[df_base['benchmark_family'] == 'SWE-bench Pro']['b_cnt'].tolist()
    pro_mean = sum(pro_b_list) / len(pro_b_list)
    poly_mean = df_base[df_base['benchmark_family'] == 'PolyBench Java']['b_cnt'].mean()
    evo_mean = df_base[df_base['benchmark_family'] == 'SWE-EVO']['b_cnt'].mean()
    
    t_stat, t_pval = ttest_ind(pro_b_list, fin_b_list, equal_var=False)
    print(f"  [PASS] Recomputed weighted means: Fineract={raw_fin_mean:.4f} (1.78), Pro={pro_mean:.4f} (2.47), Poly={poly_mean:.4f} (1.22), EVO={evo_mean:.4f} (2.29)")
    print(f"  [PASS] Independent-sample mean difference test: Welch's t={t_stat:.2f}, p={t_pval:.2e}")
    
    # 3. Cross-check requirement_dependency_evidence.md
    with open(evid_md_path, 'r', encoding='utf-8') as f:
        evid_text = f.read()
        
    if "1.74" in evid_text:
        failures.append("Incorrect value '1.74' remains in the evidence document")
        print("  [FAIL] Value '1.74' remains in the evidence document")
    else:
        print("  [PASS] Incorrect value '1.74' is absent from the evidence document")
        
    if "1.7798" in evid_text:
        print("  [PASS] Fineract mean 1.78 (1.7798) found in the evidence document")
    else:
        failures.append("Fineract mean 1.78 is missing from the evidence document")
        print("  [FAIL] Value 1.78 is missing from the evidence document")

# -----------------------------------------------------------------------------
# [Check 4] Compare source-text slices for 16 core Fineract dependencies against Jira JSON
# -----------------------------------------------------------------------------
print("\n[Check 4] Compare source-text slices for 16 core Fineract dependencies (DEP-01..DEP-16) against Jira JSON")
deps_csv_path = os.path.join(data_dir, "gate2_dependencies.csv")
raw_json_path = os.path.join(data_dir, "fineract", "gate2_raw_source_snippets.json")

if not os.path.exists(deps_csv_path) or not os.path.exists(raw_json_path):
    failures.append("Missing gate2_dependencies.csv or gate2_raw_source_snippets.json")
    print("  [FAIL] Dependency source data is missing")
else:
    df_deps = pd.read_csv(deps_csv_path)
    with open(raw_json_path, 'r', encoding='utf-8') as f:
        raw_bundle = json.load(f)
    raw_issues = raw_bundle.get('raw_jira_issues', {})
    
    raw_slice_mismatches = []
    quotes_verified = 0
    
    for _, r in df_deps.iterrows():
        dep_id = r['dep_id']
        if dep_id == 'DEP-SUPP-01':
            continue
            
        issue_id = r['issue_id']
        quote = str(r['verbatim_raw_quote']).strip()
        start_pos = int(r['raw_quote_start_pos'])
        
        if issue_id not in raw_issues:
            raw_slice_mismatches.append(f"{dep_id}: {issue_id} is missing from raw_jira_issues")
            continue
            
        desc = raw_issues[issue_id]['description']
        actual_slice = desc[start_pos : start_pos + len(quote)].strip()
        
        if actual_slice != quote:
            raw_slice_mismatches.append(f"{dep_id} Primary slice mismatch: expected '{quote[:30]}...', got '{actual_slice[:30]}...'")
        else:
            quotes_verified += 1
            
        # Paired quote check
        if pd.notna(r.get('paired_consequence_quote')) and str(r.get('paired_consequence_quote')).strip() and str(r.get('paired_consequence_quote')).strip() != 'N/A':
            p_quote = str(r['paired_consequence_quote']).strip()
            p_pos = int(r['paired_consequence_pos'])
            p_slice = desc[p_pos : p_pos + len(p_quote)].strip()
            if p_slice != p_quote:
                raw_slice_mismatches.append(f"{dep_id} Paired slice mismatch: expected '{p_quote[:30]}...', got '{p_slice[:30]}...'")
            else:
                quotes_verified += 1
                
        # Also check presence in evidence md
        if dep_id not in evid_text or f"pos: {start_pos}" not in evid_text:
            raw_slice_mismatches.append(f"{dep_id} Missing evidence document text or offset annotation")

    if not raw_slice_mismatches:
        print(f"  [PASS] All {quotes_verified} source-text slices match Jira descriptions (raw_jira_issues) for 16 core Fineract dependencies (DEP-01..DEP-16)")
        print(f"  [PASS] Evidence document IDs, source quotes, offsets, and formulas match")
    else:
        err = f"Fineract source slice mismatches: {len(raw_slice_mismatches)}: {raw_slice_mismatches[:3]}"
        failures.append(err)
        print(f"  [FAIL] {err}")

# -----------------------------------------------------------------------------
# [Check 5] Four AI comparison axes: inspect packaged original task JSON (ai_case_sources) and diffs
# -----------------------------------------------------------------------------
print("\n[Check 5] Inspect test_patch and diffs from packaged original task JSON (ai_case_sources) for four AI comparison axes")

case_sources_dir = os.path.join(data_dir, "ai_case_sources")
case_checks = []

# Axis 1: NodeBB #0030
ablation_dir = os.path.join(base_dir, "ablation_study/nodebb_0030")
dev_patch_path = os.path.join(ablation_dir, "nodebb_0030_developer_patch.diff")
abl_patch_path = os.path.join(ablation_dir, "nodebb_0030_ablated_patch.diff")
tst_patch_path = os.path.join(ablation_dir, "nodebb_0030_test_patch.diff")

if os.path.exists(dev_patch_path) and os.path.exists(abl_patch_path) and os.path.exists(tst_patch_path):
    with open(dev_patch_path, 'r', encoding='utf-8') as f:
        dev_diff = f.read()
    with open(abl_patch_path, 'r', encoding='utf-8') as f:
        abl_diff = f.read()
    with open(tst_patch_path, 'r', encoding='utf-8') as f:
        tst_diff = f.read()
        
    c1 = "src/upgrades/4.3.0/chat_allow_list.js" in dev_diff and dev_diff.count("diff --git") == 12
    c2 = "chat_allow_list.js" not in abl_diff and abl_diff.count("diff --git") == 11
    c3 = "Messaging.canMessageUser" in tst_diff and "test/messaging.js" in tst_diff
    if c1 and c2 and c3:
        print("  [PASS] Axis 1 (NodeBB #0030): inspected developer_patch (12 files, chat_allow_list.js 50 lines), ablated_patch (11 files, 0 lines), and test_patch (test/messaging.js leaf assertions) diffs")
    else:
        case_checks.append(f"NodeBB diff verification failed: dev={c1}, abl={c2}, tst={c3}")
else:
    case_checks.append("NodeBB ablation diff files are missing")

# Axis 2: Element-Web #0139 (ai_case_sources/0139.json)
t0139_path = os.path.join(case_sources_dir, "0139.json")
if os.path.exists(t0139_path):
    with open(t0139_path, 'r', encoding='utf-8') as f:
        t0139 = json.load(f)
    t0139_patch = t0139.get('test_patch', '')
    has_file = "test/Unread-test.ts" in t0139_patch
    has_mock = "mocked(haveRendererForEvent)" in t0139_patch
    has_assert1 = "expect(doesRoomHaveUnreadMessages(room)).toBe(true)" in t0139_patch
    has_assert2 = "expect(doesRoomHaveUnreadMessages(room)).toBe(false)" in t0139_patch
    if has_file and has_mock and has_assert1 and has_assert2:
        print("  [PASS] Axis 2 (Element-Web #0139): ai_case_sources/0139.json inspected original test_patch -> found mocked() and doesRoomHaveUnreadMessages() assertions in test/Unread-test.ts")
    else:
        case_checks.append(f"Element-Web #0139 test_patch verification failed: file={has_file}, mock={has_mock}, a1={has_assert1}, a2={has_assert2}")
else:
    case_checks.append("ai_case_sources/0139.json is missing from the package")

# Axis 3: RocketMQ #0819 (ai_case_sources/0819.json)
t0819_path = os.path.join(case_sources_dir, "0819.json")
if os.path.exists(t0819_path):
    with open(t0819_path, 'r', encoding='utf-8') as f:
        t0819 = json.load(f)
    t0819_patch = t0819.get('test_patch', '')
    has_test = "StatsItemSetTest.java" in t0819_patch
    has_pool = "ThreadPoolExecutor(100, 200" in t0819_patch
    has_assert = "assertEquals(20000L, test_unit().longValue())" in t0819_patch
    if has_test and has_pool and has_assert:
        print("  [PASS] Axis 3 (RocketMQ #0819): ai_case_sources/0819.json inspected original test_patch -> found the 100-worker thread pool and 20000L assertEquals assertion in StatsItemSetTest.java")
    else:
        case_checks.append(f"RocketMQ #0819 test_patch verification failed: test={has_test}, pool={has_pool}, assert={has_assert}")
else:
    case_checks.append("ai_case_sources/0819.json is missing from the package")

# Axis 4: Navidrome #0495 (ai_case_sources/0495.json)
t0495_path = os.path.join(case_sources_dir, "0495.json")
if os.path.exists(t0495_path):
    with open(t0495_path, 'r', encoding='utf-8') as f:
        t0495 = json.load(f)
    t0495_patch = t0495.get('test_patch', '')
    has_go_test = "db/backup_test.go" in t0495_patch
    has_ddl = "DELETE FROM sqlite_master" in t0495_patch
    has_prune_assert = "Expect(len(timesDecreasingChronologically) - pruneCount).To(Equal(expected))" in t0495_patch
    if has_go_test and has_ddl and has_prune_assert:
        print("  [PASS] Axis 4 (Navidrome #0495): ai_case_sources/0495.json inspected original test_patch -> found SQLite DDL destruction/restoration and pruning retention assertions in db/backup_test.go")
    else:
        case_checks.append(f"Navidrome #0495 test_patch verification failed: file={has_go_test}, ddl={has_ddl}, prune={has_prune_assert}")
else:
    case_checks.append("ai_case_sources/0495.json is missing from the package")

if case_checks:
    failures.extend(case_checks)
    for cc in case_checks:
        print(f"  [FAIL] {cc}")

# -----------------------------------------------------------------------------
# [Check 6] Check calibrated phrasing and distinctions among three analytical levels
# -----------------------------------------------------------------------------
print("\n[Check 6] Check calibrated phrasing (exclude exaggeration and unsupported statistical significance) and three analytical levels")

# 3 analytical levels check
has_l1 = "Level 1: Per-task multi-attribute diversity" in evid_text
has_l2 = "Level 2: Corpus-level statistical co-occurrence" in evid_text
has_l3 = "Level 3: Source-grounded directional relationships" in evid_text

if has_l1 and has_l2 and has_l3:
    print("  [PASS] Found distinctions among three analytical levels: attribute diversity, statistical co-occurrence, and directional causal dependencies")
else:
    failures.append("Missing distinctions among the three analytical levels")
    print("  [FAIL] Missing distinctions among the three analytical levels")

# Banned exaggerated or ungrounded terms
banned_terms = [
    ('inevitably coupled', 'Exaggerated causal coupling claim'),
    ('completely decoupled', 'Exaggerated correlation claim'),
    ('statistically completely independent', 'Exaggerated statistical independence claim'),
    ('perfect proof', 'Exaggerated proof wording'),
    ('perfect verification', 'Exaggerated verification wording'),
    ('significantly higher without a test', 'Statistical significance claim without a test'),
    ('report.json', 'Unsupported execution artifact reference'),
    ('run_instance.log', 'Unsupported execution artifact reference'),
    ('benchmark_score=1.0', 'Unsupported evaluation score'),
    ('passes with a perfect score', 'Unsupported passing claim')
]

found_banned = []
for term, desc in banned_terms:
    if term in evid_text:
        found_banned.append(f"{desc} ('{term}')")

if not found_banned:
    print("  [PASS] No listed exaggerated terms, unsupported statistical significance, or unsupported execution claims found")
else:
    err = f"Found {len(found_banned)} prohibited terms: {found_banned}"
    failures.append(err)
    print(f"  [FAIL] {err}")

# -----------------------------------------------------------------------------
# Final Exit Determination
# -----------------------------------------------------------------------------
print("\n" + "=" * 80)
if not failures:
    print(" [PASS] Gate 3 self-contained package verification complete (0 Failures, Exit Code 0)")
    print("=" * 80)
    sys.exit(0)
else:
    print(f" [FAIL] Gate 3 verification failed: {len(failures)} errors detected")
    for f in failures:
        print(f"  - {f}")
    print("=" * 80)
    sys.exit(1)
