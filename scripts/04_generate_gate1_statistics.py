import os, csv, json, math
import scipy.stats as stats

paper_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(paper_dir, "data")

# 1. Load Fineract counts from summary.json
summary_file = os.path.join(data_dir, "fineract", "summary.json")
with open(summary_file, 'r', encoding='utf-8') as f:
    sum_data = json.load(f)

N_fin = sum_data.get('source_issues', 2925)
fineract_counts = {e['code']: e['issue_count'] for e in sum_data['entries']}

# 2. Load the source codebook; use English display names in the output table.
fs_file = os.path.join(data_dir, "framework-snapshot.json")
with open(fs_file, 'r', encoding='utf-8') as f:
    fs_data = json.load(f)
code_to_name = {e['code']: e['name'] for e in fs_data['entries']}
english_names = {
    'A1': 'Product behavior and business rules',
    'A2': 'Structure and implementation approach',
    'A3': 'Testing and quality assurance',
    'A4': 'Execution and operations',
    'A5': 'Deployment, version, and environment transitions',
    'A6': 'Development process, documentation, and project support',
    'B1': 'Functional results and input conditions',
    'B2': 'Numerical and calculation accuracy',
    'B3': 'Data relationships and consistency',
    'B4': 'Temporal and ordering semantics',
    'B5': 'State and business workflows',
    'B6': 'Preservation of existing information and behavior',
    'B7': 'Concurrent execution and transaction boundaries',
    'B8': 'Authorization and protection',
    'B9': 'Performance and resource use',
    'B10': 'Service continuity and failure handling',
    'B11': 'Interface and environment compatibility',
    'B12': 'User interaction',
}

# 3. Load baseline_tasks.csv for total AI tasks count
baseline_csv = os.path.join(data_dir, "baseline_tasks.csv")
with open(baseline_csv, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    baseline_rows = list(reader)
N_ai = len(baseline_rows) # 944

# 4. Load ab_long.csv to count AI tasks evaluating each criterion
ab_csv = os.path.join(data_dir, "ab_long.csv")
ai_counts = {code: 0 for code in code_to_name}
with open(ab_csv, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for r in reader:
        c = r['criterion_code']
        if c in ai_counts:
            ai_counts[c] += 1

# 5. Generate Markdown Table
codes_order = [f"A{i}" for i in range(1, 7)] + [f"B{i}" for i in range(1, 13)]
alpha_bonferroni = 0.05 / 18 # ~0.002778

lines = []
lines.append(f"| Code | Criterion (English description) | Fineract (N={N_fin:,}) | AI 944 (N={N_ai:,}) | Odds Ratio (95% CI) | Fisher p-value | Higher In |")
lines.append("| :---: | :--- | :---: | :---: | :---: | :---: | :---: |")

stat_summary = {
    'fineract_higher': 0,
    'ai_higher': 0,
    'not_significant': 0
}

for code in codes_order:
    name = english_names[code]
    a = fineract_counts[code]
    b = N_fin - a
    c = ai_counts[code]
    d = N_ai - c
    
    odds, p_val = stats.fisher_exact([[a, b], [c, d]])
    
    se = math.sqrt(1.0/a + 1.0/b + 1.0/c + 1.0/d)
    log_or = math.log(odds)
    ci_low = math.exp(log_or - 1.96 * se)
    ci_high = math.exp(log_or + 1.96 * se)
    
    fin_pct = (a / N_fin) * 100
    ai_pct = (c / N_ai) * 100
    
    p_str = f"{p_val:.2e}" if p_val < 0.0001 else f"{p_val:.4f}"
    
    if p_val >= alpha_bonferroni:
        higher = "No significant difference (n.s.)"
        stat_summary['not_significant'] += 1
    elif odds > 1:
        higher = "**Higher in Fineract**"
        stat_summary['fineract_higher'] += 1
    else:
        higher = "**Higher in AI 944**"
        stat_summary['ai_higher'] += 1
        
    line = f"| **{code}** | {name} | {a} ({fin_pct:.2f}%) | {c} ({ai_pct:.2f}%) | {odds:.2f} [{ci_low:.2f}, {ci_high:.2f}] | {p_str} | {higher} |"
    lines.append(line)

table_content = "\n".join(lines) + "\n"

# 6. Save gate1_verified_table.md
out_md = os.path.join(paper_dir, "evidence", "gate1_verified_table.md")
with open(out_md, 'w', encoding='utf-8') as f:
    f.write(table_content)

print(f"Generated: {out_md}")
print(f"Summary: Fineract Higher={stat_summary['fineract_higher']}, AI 944 Higher={stat_summary['ai_higher']}, Non-significant={stat_summary['not_significant']}")
print(f"Bonferroni threshold (alpha = 0.05 / 18): {alpha_bonferroni:.6f}")
