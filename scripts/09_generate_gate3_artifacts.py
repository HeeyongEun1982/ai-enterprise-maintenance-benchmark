"""
09. Gate 3 Quantitative Stratification & Statistical Artifact Generator
Generates:
1. gate3_stratified_family_metrics.csv (SWE-bench Pro 731, PolyBench 165, SWE-EVO 48 breakdown)
2. gate3_phi_correlation_matrix.csv (Phi correlation, co-occurrence counts, and p-values)
3. gate3_coupling_complexity.csv (|B| multi-attribute coupling complexity distributions)
"""

import os
import sys
import json
import csv
import math
import pandas as pd
from collections import defaultdict
from scipy.stats import fisher_exact

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(base_dir, "data")

print("=" * 80)
print(" 09. GENERATING GATE 3 QUANTITATIVE ARTIFACTS & STRATIFIED METRICS")
print("=" * 80)

# -----------------------------------------------------------------------------
# 1. Load Data
# -----------------------------------------------------------------------------
codebook_path = os.path.join(data_dir, "framework-snapshot.json")
with open(codebook_path, 'r', encoding='utf-8') as f:
    cb_data = json.load(f)
cb_map = {e['code']: e['name'] for e in cb_data['entries']}

expected_codes = [
    'A1', 'A2', 'A3', 'A4', 'A5', 'A6',
    'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11', 'B12'
]

fin_summary_path = os.path.join(data_dir, "fineract", "summary.json")
with open(fin_summary_path, 'r', encoding='utf-8') as f:
    fin_summary = json.load(f)

fin_issue_codes = defaultdict(set)
for entry in fin_summary.get('entries', []):
    code = entry.get('code')
    for u in entry.get('all_unit_ids', []):
        iid = u.split('-R')[0]
        fin_issue_codes[iid].add(code)
total_fin = 2925

base_csv_path = os.path.join(data_dir, "baseline_tasks.csv")
ab_long_path = os.path.join(data_dir, "ab_long.csv")
df_base = pd.read_csv(base_csv_path)
df_ab = pd.read_csv(ab_long_path)
total_ai = len(df_base)

ai_task_codes = defaultdict(set)
for _, r in df_ab.iterrows():
    ai_task_codes[int(r['task_id'])].add(r['criterion_code'])

# -----------------------------------------------------------------------------
# 2. Artifact 1: Stratified Benchmark Family Metrics
# -----------------------------------------------------------------------------
print("\n[Artifact 1] Generating gate3_stratified_family_metrics.csv...")
df_merged = df_ab.merge(df_base[['task_id', 'benchmark_family']], on='task_id')
families = ['SWE-bench Pro', 'PolyBench Java', 'SWE-EVO']
family_totals = df_base['benchmark_family'].value_counts().to_dict()

strat_rows = []
for c in expected_codes:
    row = {
        'criterion_code': c,
        'criterion_name': cb_map[c],
        'all_tasks_count': len(df_ab[df_ab['criterion_code'] == c]),
        'all_tasks_pct': round((len(df_ab[df_ab['criterion_code'] == c]) / total_ai) * 100.0, 2),
    }
    for fam in families:
        tot = family_totals[fam]
        cnt = len(df_merged[(df_merged['criterion_code'] == c) & (df_merged['benchmark_family'] == fam)])
        row[f'{fam}_count'] = cnt
        row[f'{fam}_pct'] = round((cnt / tot) * 100.0, 2)
    strat_rows.append(row)

df_strat = pd.DataFrame(strat_rows)
strat_csv_path = os.path.join(data_dir, "gate3_stratified_family_metrics.csv")
df_strat.to_csv(strat_csv_path, index=False, encoding='utf-8', lineterminator='\r\n')
print(f"  -> Saved {len(df_strat)} rows to {strat_csv_path}")

# -----------------------------------------------------------------------------
# 3. Artifact 2: Phi Correlation Matrix & Causal Chains
# -----------------------------------------------------------------------------
print("\n[Artifact 2] Generating gate3_phi_correlation_matrix.csv...")
def get_contingency_and_phi(dataset_codes, total_n, c1, c2):
    n11 = sum(1 for codes in dataset_codes.values() if c1 in codes and c2 in codes)
    n10 = sum(1 for codes in dataset_codes.values() if c1 in codes and c2 not in codes)
    n01 = sum(1 for codes in dataset_codes.values() if c1 not in codes and c2 in codes)
    n00 = total_n - (n11 + n10 + n01)
    
    num = (n11 * n00) - (n10 * n01)
    den = math.sqrt((n11 + n10) * (n01 + n00) * (n11 + n01) * (n10 + n00))
    phi = num / den if den > 0 else 0.0
    
    table = [[n11, n10], [n01, n00]]
    _, p_val = fisher_exact(table)
    return n11, phi, p_val

target_pairs = [
    ('B4', 'B2', '소급 변경 -> 수치 연쇄 재계산 (Temporal Retroactive -> Numerical Recalculation)'),
    ('A1', 'B4', '업무 규칙 -> 시간적 소급 적용 (Business Rule -> Temporal Retroactive)'),
    ('A1', 'B2', '업무 규칙 -> 복합 수치 산출 (Business Rule -> Numerical Recalculation)'),
    ('A1', 'B3', '업무 규칙 -> 데이터 관계 정합성 (Business Rule -> Data Consistency)'),
    ('B4', 'B3', '시간 소급 -> 상태 정합성 (Temporal Retroactive -> State Consistency)'),
    ('B4', 'B6', '시간 소급 -> 상태 보존 (Temporal Retroactive -> State Preservation)'),
    ('B2', 'B3', '수치 재산출 -> 원장 정합성 (Numerical Recalculation -> Data Integrity)'),
    ('B2', 'B6', '수치 재산출 -> 상태 보존 (Numerical Recalculation -> State Preservation)'),
    ('B3', 'B6', '정합성 유지 -> 상태 불변 보존 (Data Integrity -> State Preservation)'),
    ('B7', 'B6', '트랜잭션 격리 -> 상태 보존 (Transaction Isolation -> State Preservation)'),
    ('B7', 'B3', '트랜잭션 격리 -> 원장 무결성 (Transaction Isolation -> Data Integrity)')
]

phi_rows = []
for c1, c2, desc in target_pairs:
    f_co, f_phi, f_p = get_contingency_and_phi(fin_issue_codes, total_fin, c1, c2)
    a_co, a_phi, a_p = get_contingency_and_phi(ai_task_codes, total_ai, c1, c2)
    phi_rows.append({
        'pair': f"{c1}-{c2}",
        'c1': c1,
        'c2': c2,
        'semantic_chain': desc,
        'fineract_cooccurrence': f_co,
        'fineract_phi': round(f_phi, 3),
        'fineract_p_value': f_p,
        'ai_cooccurrence': a_co,
        'ai_phi': round(a_phi, 3),
        'ai_p_value': a_p
    })

df_phi = pd.DataFrame(phi_rows)
phi_csv_path = os.path.join(data_dir, "gate3_phi_correlation_matrix.csv")
df_phi.to_csv(phi_csv_path, index=False, encoding='utf-8', lineterminator='\r\n')
print(f"  -> Saved {len(df_phi)} pairs to {phi_csv_path}")

# -----------------------------------------------------------------------------
# 4. Artifact 3: Multi-Criteria Coupling Complexity (|B|)
# -----------------------------------------------------------------------------
print("\n[Artifact 3] Generating gate3_coupling_complexity.csv...")
b_codes = set([c for c in expected_codes if c.startswith('B')])

fin_b_dist = defaultdict(int)
for iid in fin_issue_codes:
    b_cnt = len({c for c in fin_issue_codes[iid] if c.startswith('B')})
    fin_b_dist[b_cnt] += 1
fin_b_dist[0] += (total_fin - len(fin_issue_codes))

b_counts_per_task = df_ab[df_ab['criterion_code'].isin(b_codes)].groupby('task_id')['criterion_code'].count().to_dict()
for tid in df_base['task_id']:
    if tid not in b_counts_per_task:
        b_counts_per_task[tid] = 0
df_base['b_count'] = df_base['task_id'].map(b_counts_per_task)

coupling_rows = []
for k in range(0, 9):
    f_cnt = fin_b_dist.get(k, 0)
    ai_all_cnt = len(df_base[df_base['b_count'] == k])
    row = {
        'b_complexity': f"|B| = {k}",
        'fineract_count': f_cnt,
        'fineract_pct': round((f_cnt / total_fin) * 100.0, 2),
        'ai_all_count': ai_all_cnt,
        'ai_all_pct': round((ai_all_cnt / total_ai) * 100.0, 2),
    }
    for fam in families:
        sub = df_base[df_base['benchmark_family'] == fam]
        sub_cnt = len(sub[sub['b_count'] == k])
        row[f'{fam}_count'] = sub_cnt
        row[f'{fam}_pct'] = round((sub_cnt / len(sub)) * 100.0, 2)
    coupling_rows.append(row)

df_coupling = pd.DataFrame(coupling_rows)
coupling_csv_path = os.path.join(data_dir, "gate3_coupling_complexity.csv")
df_coupling.to_csv(coupling_csv_path, index=False, encoding='utf-8', lineterminator='\r\n')
print(f"  -> Saved {len(df_coupling)} complexity rows to {coupling_csv_path}")

print("\n" + "=" * 80)
print(" GATE 3 ARTIFACT GENERATION COMPLETED SUCCESSFULLY")
print("=" * 80)
