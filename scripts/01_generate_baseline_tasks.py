import json, os, csv, re
from collections import Counter

import argparse
from pathlib import Path
parser = argparse.ArgumentParser(description="Optional rebuild; requires the original RAW5 source tree, which is not included in this release.")
parser.add_argument("--raw5", type=Path, required=True, help="Path to the original RAW5 input directory")
parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parents[1] / "data")
args = parser.parse_args()
raw5_dir = str(args.raw5.expanduser().resolve())
data_dir = str(args.output_dir.expanduser().resolve())
os.makedirs(data_dir, exist_ok=True)

# 1. Load comparison.json for benchmark family mapping
comp_file = os.path.join(raw5_dir, "03_AI944개_전체_비교평가/comparison/maintenance18-ai944/comparison.json")
with open(comp_file, 'r', encoding='utf-8') as f:
    comp_data = json.load(f)

comp_by_index = {}
for item in comp_data:
    idx = item.get('index')
    raw_b = item.get('benchmark', '')
    if 'PolyBench' in raw_b or 'Multilingual' in raw_b:
        family = "PolyBench Java"
    elif 'EVO' in raw_b:
        family = "SWE-EVO"
    else:
        family = "SWE-bench Pro"
    comp_by_index[idx] = family

raw_tasks_dir = os.path.join(raw5_dir, "03_AI944개_전체_비교평가/comparison/se-ai-comparison/tasks")
task_files = [f"{i+1:04d}.json" for i in range(944)]

baseline_tasks = []
multilabel_count = 0

for i, fname in enumerate(task_files):
    t_idx = i + 1
    t_id = f"{t_idx:04d}"
    t_path = os.path.join(raw_tasks_dir, fname)
    with open(t_path, 'r', encoding='utf-8') as tf:
        td = json.load(tf)
        
    patch = td.get('patch', '')
    added = len(re.findall(r'^\+[^+]', patch, re.MULTILINE))
    deleted = len(re.findall(r'^-[^-]', patch, re.MULTILINE))
    diff_files = len(re.findall(r'^diff --git', patch, re.MULTILINE))
    if diff_files == 0 and patch:
        diff_files = 1
        
    family = comp_by_index.get(t_idx, "SWE-bench Pro")
    
    # Extract native types:
    # 1. PolyBench uses task_category (single label)
    # 2. SWE-bench Pro uses issue_specificity (array)
    # 3. SWE-EVO has neither (unknown)
    primary_type = "unknown"
    full_types_list = []
    
    if family == "PolyBench Java" and td.get('task_category'):
        primary_type = td.get('task_category')
        full_types_list = [primary_type]
    elif td.get('issue_specificity'):
        spec = td.get('issue_specificity')
        if isinstance(spec, str) and spec.startswith('['):
            try:
                spec_list = json.loads(spec.replace("'", '"'))
                full_types_list = spec_list
                primary_type = spec_list[0] if spec_list else "unknown"
            except:
                full_types_list = [spec]
                primary_type = spec
        elif isinstance(spec, list):
            full_types_list = spec
            primary_type = spec[0] if spec else "unknown"
        else:
            full_types_list = [str(spec)]
            primary_type = str(spec)
    elif td.get('task_category'):
        primary_type = td.get('task_category')
        full_types_list = [primary_type]
        
    if len(full_types_list) > 1:
        multilabel_count += 1

    baseline_tasks.append({
        'task_id': t_id,
        'repo': td.get('repo', ''),
        'instance_id': td.get('instance_id', ''),
        'benchmark_family': family,
        'repo_language': td.get('repo_language', td.get('language', '')),
        'primary_issue_type': primary_type,
        'native_issue_types': json.dumps(full_types_list, ensure_ascii=False),
        'patch_files_count': diff_files,
        'patch_loc_added': added,
        'patch_loc_deleted': deleted,
        'patch_loc_total': added + deleted
    })

# Write updated baseline_tasks.csv
baseline_csv = os.path.join(data_dir, "baseline_tasks.csv")
with open(baseline_csv, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(baseline_tasks[0].keys()))
    writer.writeheader()
    writer.writerows(baseline_tasks)

print(f"Generated: {baseline_csv}")
print(f"Total multi-label tasks preserved: {multilabel_count} (out of 731 Pro tasks: 576)")

