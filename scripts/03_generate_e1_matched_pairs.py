import os, csv, json, math
from collections import defaultdict

paper_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(paper_dir, "data")

baseline = []
with open(os.path.join(data_dir, "baseline_tasks.csv"), 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for r in reader:
        r['patch_files_count'] = int(r['patch_files_count'])
        r['patch_loc_total'] = int(r['patch_loc_total'])
        baseline.append(r)

task_b_criteria = defaultdict(set)
with open(os.path.join(data_dir, "ab_long.csv"), 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for r in reader:
        code = r['criterion_code']
        if code.startswith('B'):
            task_b_criteria[r['task_id']].add(code)

def jaccard_dist(s1, s2):
    if not s1 and not s2:
        return 0.0
    union = s1.union(s2)
    inter = s1.intersection(s2)
    return 1.0 - (len(inter) / len(union))

matched_pairs = []
unique_tasks = set()
pro_pairs = 0
poly_pairs = 0

for i in range(len(baseline)):
    for j in range(i + 1, len(baseline)):
        t1 = baseline[i]
        t2 = baseline[j]
        # Match only on primary_issue_type if valid
        if t1['primary_issue_type'] == 'unknown' or t2['primary_issue_type'] == 'unknown':
            continue
        if t1['primary_issue_type'] == t2['primary_issue_type']:
            if t1['patch_files_count'] == t2['patch_files_count']:
                loc1 = t1['patch_loc_total']
                loc2 = t2['patch_loc_total']
                diff = abs(loc1 - loc2)
                threshold = max(3, int(0.3 * max(loc1, loc2)))
                if diff <= threshold:
                    b1 = task_b_criteria[t1['task_id']]
                    b2 = task_b_criteria[t2['task_id']]
                    if b1 or b2:
                        d_j = jaccard_dist(b1, b2)
                        matched_pairs.append({
                            'pair_id': len(matched_pairs) + 1,
                            'task_id_1': t1['task_id'],
                            'repo_1': t1['repo'],
                            'family_1': t1['benchmark_family'],
                            'primary_type_1': t1['primary_issue_type'],
                            'files_1': t1['patch_files_count'],
                            'loc_1': loc1,
                            'b_codes_1': ";".join(sorted(list(b1))),
                            'task_id_2': t2['task_id'],
                            'repo_2': t2['repo'],
                            'family_2': t2['benchmark_family'],
                            'primary_type_2': t2['primary_issue_type'],
                            'files_2': t2['patch_files_count'],
                            'loc_2': loc2,
                            'b_codes_2': ";".join(sorted(list(b2))),
                            'jaccard_distance': round(d_j, 4)
                        })
                        unique_tasks.add(t1['task_id'])
                        unique_tasks.add(t2['task_id'])
                        if t1['benchmark_family'] == 'SWE-bench Pro' and t2['benchmark_family'] == 'SWE-bench Pro':
                            pro_pairs += 1
                        elif t1['benchmark_family'] == 'PolyBench Java' and t2['benchmark_family'] == 'PolyBench Java':
                            poly_pairs += 1

e1_csv = os.path.join(data_dir, "e1_matched_pairs.csv")
with open(e1_csv, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(matched_pairs[0].keys()))
    writer.writeheader()
    writer.writerows(matched_pairs)

N_pairs = len(matched_pairs)
mean_j = sum(p['jaccard_distance'] for p in matched_pairs) / N_pairs
median_j = sorted([p['jaccard_distance'] for p in matched_pairs])[N_pairs // 2]
var_j = sum((p['jaccard_distance'] - mean_j) ** 2 for p in matched_pairs) / (N_pairs - 1)
sd_j = math.sqrt(var_j)
disjoint_count = sum(1 for p in matched_pairs if p['jaccard_distance'] >= 0.999)

print(f"Generated: {e1_csv}")
print(f"Total Matched Pairs: {N_pairs} (SWE-bench Pro: {pro_pairs}, PolyBench Java: {poly_pairs}, Cross-family: {N_pairs - pro_pairs - poly_pairs})")
print(f"Unique tasks participating in pairs: {len(unique_tasks)}")
print(f"Mean Jaccard Distance: {mean_j:.4f}, Median: {median_j:.4f}, SD: {sd_j:.4f}")
print(f"Completely Disjoint Pairs: {disjoint_count} ({disjoint_count / N_pairs * 100:.2f}%)")
