#!/usr/bin/env python3
"""
Master Verification Script for Replication Package:
Beyond Surface Metrics: Multi-Condition Requirements in Enterprise Maintenance and AI Coding Benchmarks
Submitting to BenchSOC 2026 / ICSOC 2026

This script performs six numerical and structural consistency checks for a subset
of paper claims. It does not validate independent annotators, semantic correctness,
external source licenses, or benchmark runtime scores.
"""

import sys
import json
import math
import pandas as pd
from pathlib import Path
from scipy.stats import ttest_ind

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
EVIDENCE_DIR = REPO_ROOT / "evidence"

def verify_census_counts():
    print("[1/6] Verifying Census Task Counts & Annotation Volumes...")
    ab_long_file = DATA_DIR / "ab_long.csv"
    assert ab_long_file.exists(), f"Missing {ab_long_file}"
    df = pd.read_csv(ab_long_file)
    
    with open(DATA_DIR / "framework-snapshot.json", encoding="utf-8") as f:
        codebook = {e["code"]: e["name"] for e in json.load(f)["entries"]}
    assert len(codebook) == 18, "Expected frozen 18-criterion codebook"
    assert set(df["criterion_code"]).issubset(codebook), "Unexpected criterion codes"
    mismatches = df[df.apply(lambda row: str(row["criterion_name"]) != codebook[row["criterion_code"]], axis=1)]
    assert mismatches.empty, f"Codebook name mismatch in {len(mismatches)} rows"
    total_annotations = len(df)
    unique_tasks = df['task_id'].nunique()
    
    print(f"  - Total criteria assignments: {total_annotations} (Paper: 3,446)")
    print(f"  - Unique AI benchmark tasks: {unique_tasks} (Paper: 944)")
    
    assert total_annotations == 3446, f"Expected 3,446 annotations, got {total_annotations}"
    assert unique_tasks == 944, f"Expected 944 unique tasks, got {unique_tasks}"
    print("  --> PASS: Census volumes exactly match paper specification.\n")

def verify_e1_matched_pairs():
    print("[2/6] Verifying E1: Controlled Matched-Pair Churn Analysis (N=1,177)...")
    pairs_file = DATA_DIR / "e1_matched_pairs.csv"
    assert pairs_file.exists(), f"Missing {pairs_file}"
    df_pairs = pd.read_csv(pairs_file)
    
    total_pairs = len(df_pairs)
    mean_dj = df_pairs['jaccard_distance'].mean()
    median_dj = df_pairs['jaccard_distance'].median()
    disjoint_pairs = (df_pairs['jaccard_distance'] == 1.0).sum()
    disjoint_ratio = disjoint_pairs / total_pairs * 100.0
    
    print(f"  - Total controlled matched pairs: {total_pairs} (Paper: 1,177)")
    print(f"  - Mean Jaccard distance (d_J): {mean_dj:.4f} (Paper: 0.8138)")
    print(f"  - Median Jaccard distance: {median_dj:.4f} (Paper: 1.0000)")
    print(f"  - Completely disjoint pairs (d_J = 1.0): {disjoint_pairs} ({disjoint_ratio:.1f}%) (Paper: 676, 57.4%)")
    
    assert total_pairs == 1177, f"Expected 1,177 pairs, got {total_pairs}"
    assert abs(mean_dj - 0.8138) < 0.001, f"Expected mean d_J ~ 0.8138, got {mean_dj}"
    assert disjoint_pairs == 676, f"Expected 676 disjoint pairs, got {disjoint_pairs}"
    print("  --> PASS: E1 matched-pair summary checks.\n")

def verify_table2_stratified():
    print("[3/6] Verifying Table 2: Stratified 18-Criteria Distribution Across Benchmark Families...")
    t2_file = DATA_DIR / "gate3_stratified_family_metrics.csv"
    assert t2_file.exists(), f"Missing {t2_file}"
    df_t2 = pd.read_csv(t2_file)
    
    # Check key criteria reported in paper
    # A1: AI All = 426 (45.13%), Pro = 300 (41.04%), Poly = 84 (50.91%), EVO = 42 (87.50%)
    row_a1 = df_t2[df_t2['criterion_code'] == 'A1'].iloc[0]
    print(f"  - Criterion A1: AI All={row_a1['all_tasks_count']}, Pro={row_a1['SWE-bench Pro_count']}, Poly={row_a1['PolyBench Java_count']}, EVO={row_a1['SWE-EVO_count']}")
    assert row_a1['all_tasks_count'] == 426
    assert row_a1['SWE-bench Pro_count'] == 300
    assert row_a1['PolyBench Java_count'] == 84
    assert row_a1['SWE-EVO_count'] == 42
    
    # B6: AI All = 368 (38.98%), Pro = 336 (45.96%)
    row_b6 = df_t2[df_t2['criterion_code'] == 'B6'].iloc[0]
    print(f"  - Criterion B6: AI All={row_b6['all_tasks_count']}, Pro={row_b6['SWE-bench Pro_count']}")
    assert row_b6['all_tasks_count'] == 368
    assert row_b6['SWE-bench Pro_count'] == 336
    print("  --> PASS: Table 2 stratified distribution counts verified.\n")

def verify_table3_coupling():
    print("[4/6] Verifying Table 3: Multi-Attribute Co-presence Complexity (|B|)...")
    t3_file = DATA_DIR / "gate3_coupling_complexity.csv"
    base_file = DATA_DIR / "baseline_tasks.csv"
    ab_file = DATA_DIR / "ab_long.csv"
    assert t3_file.exists() and base_file.exists() and ab_file.exists()
    
    df_t3 = pd.read_csv(t3_file)
    df_base = pd.read_csv(base_file)
    df_ab = pd.read_csv(ab_file)
    
    # Verify bin 0..8 totals
    assert len(df_t3) == 9
    expected_counts = {"fineract_count": 2925, "ai_all_count": 944, "SWE-bench Pro_count": 731, "PolyBench Java_count": 165, "SWE-EVO_count": 48}
    for column, expected in expected_counts.items():
        assert int(df_t3[column].sum()) == expected, f"Table 3 {column} subtotal does not sum to {expected}"
    
    ai_all_weighted = sum(int(row['b_complexity'].split('=')[1]) * row['ai_all_count'] for _, row in df_t3.iterrows())
    ai_all_total = df_t3['ai_all_count'].sum()
    ai_all_mean = ai_all_weighted / ai_all_total

    pro_weighted = sum(int(row['b_complexity'].split('=')[1]) * row['SWE-bench Pro_count'] for _, row in df_t3.iterrows())
    pro_total = df_t3['SWE-bench Pro_count'].sum()
    pro_mean = pro_weighted / pro_total

    poly_weighted = sum(int(row['b_complexity'].split('=')[1]) * row['PolyBench Java_count'] for _, row in df_t3.iterrows())
    poly_total = df_t3['PolyBench Java_count'].sum()
    poly_mean = poly_weighted / poly_total

    evo_weighted = sum(int(row['b_complexity'].split('=')[1]) * row['SWE-EVO_count'] for _, row in df_t3.iterrows())
    evo_total = df_t3['SWE-EVO_count'].sum()
    evo_mean = evo_weighted / evo_total

    # Fineract distribution from CSV
    fin_weighted_sum = sum(int(row['b_complexity'].split('=')[1]) * row['fineract_count'] for _, row in df_t3.iterrows())
    fin_total = df_t3['fineract_count'].sum()
    fin_mean = fin_weighted_sum / fin_total
    
    print(f"  - Mean |B| (Fineract): {fin_mean:.4f} (Paper: 1.78 / 1.7798)")
    print(f"  - Mean |B| (AI All):   {ai_all_mean:.4f} (from frozen bins: 2.2447)")
    print(f"  - Mean |B| (SWE Pro):  {pro_mean:.4f} (Paper: 2.47 / 2.4733)")
    print(f"  - Mean |B| (PolyJava): {poly_mean:.4f} (Paper: 1.22 / 1.2182)")
    print(f"  - Mean |B| (SWE-EVO):  {evo_mean:.4f} (Paper: 2.29 / 2.2917)")
    
    assert abs(fin_mean - 1.7798) < 0.001
    assert abs(ai_all_mean - 2.2447) < 0.0001
    assert abs(pro_mean - 2.4733) < 0.001
    assert abs(poly_mean - 1.2182) < 0.001
    assert abs(evo_mean - 2.2917) < 0.001
    print("  --> PASS: Table 3 mean and subtotal consistency checks.\n")

def verify_table4_phi():
    print("[5/6] Verifying Table 4: Corpus-Level Linear Co-occurrence (Phi)...")
    t4_file = DATA_DIR / "gate3_phi_correlation_matrix.csv"
    assert t4_file.exists(), f"Missing {t4_file}"
    df_t4 = pd.read_csv(t4_file)
    
    # Key pair: B4 <-> B2
    # Fineract: 254 co-occurrences, phi = +0.430
    # AI Benchmarks: 5 co-occurrences, phi = -0.013, p = 0.825
    b4_b2 = df_t4[(df_t4['c1'] == 'B4') & (df_t4['c2'] == 'B2')].iloc[0]
    print(f"  - Pair B4 <-> B2:")
    print(f"    * Fineract: {b4_b2['fineract_cooccurrence']} issues, phi = {b4_b2['fineract_phi']:+.3f}")
    print(f"    * AI Benchmarks: {b4_b2['ai_cooccurrence']} tasks, phi = {b4_b2['ai_phi']:+.3f} (p = {b4_b2['ai_p_value']:.3f})")
    
    assert b4_b2['fineract_cooccurrence'] == 254
    assert abs(b4_b2['fineract_phi'] - 0.430) < 0.005
    assert b4_b2['ai_cooccurrence'] == 5
    assert abs(b4_b2['ai_phi'] - (-0.013)) < 0.005
    print("  --> PASS: Table 4 phi correlation divergence verified.\n")

def verify_fineract_dependencies():
    print("[6/6] Verifying Table 5 & Evidence: Apache Fineract 16 Business Dependency Chains...")
    dep_file = DATA_DIR / "gate2_dependencies.csv"
    snippet_file = DATA_DIR / "fineract" / "gate2_raw_source_snippets.json"
    assert dep_file.exists(), f"Missing {dep_file}"
    assert snippet_file.exists(), f"Missing {snippet_file}"
    
    df_dep = pd.read_csv(dep_file)
    with open(snippet_file, "r", encoding="utf-8") as f:
        snippets = json.load(f)
        
    groundings = snippets.get('verified_dependency_grounding', [])
    print(f"  - Total documented dependency chains: {len(df_dep)} (16 business + 1 build environment)")
    print(f"  - Byte-verified Jira requirement snippets: {len(groundings)} quotes")
    assert len(groundings) == 17
    
    # Check FINERACT-2338 multi-tier cascade
    fineract_2338_rows = df_dep[df_dep['issue_id'] == 'FINERACT-2338']
    print(f"  - FINERACT-2338 cascade links: {len(fineract_2338_rows)} verified dependencies")
    assert len(fineract_2338_rows) >= 4
    print("  --> PASS: Fineract dependency traceability verified.\n")

def main():
    print("================================================================================")
    print("Replication Package Automated Verification")
    print("Paper: Beyond Surface Metrics: Multi-Condition Requirements in Enterprise Maintenance and AI Coding Benchmarks")
    print("Target: BenchSOC 2026 / ICSOC 2026")
    print("================================================================================\n")
    
    try:
        verify_census_counts()
        verify_e1_matched_pairs()
        verify_table2_stratified()
        verify_table3_coupling()
        verify_table4_phi()
        verify_fineract_dependencies()
        print("================================================================================")
        print("ALL SIX DECLARED CONSISTENCY CHECKS PASSED (NOT AN INDEPENDENT SEMANTIC AUDIT).")
        print("================================================================================")
    except AssertionError as e:
        print(f"\n[FAIL] Verification error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
