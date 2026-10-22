"""원본 과제 944개의 메타데이터와 정답 패치의 변경 규모를 CSV로 추출한다.

입력: data/inputs의 벤치마크 구분 정보와 과제별 JSON 파일.
출력: data/baseline_tasks.csv. --output-dir로 다른 저장 위치를 지정할 수 있다.
기존 출력 파일이 있으면 덮어쓴다.
"""

import json, os, csv, re
from collections import Counter

import argparse
from pathlib import Path
repo_root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description="패키지에 포함된 원본 입력으로 과제 기본 정보 CSV를 재생성합니다.")
inputs = parser.add_mutually_exclusive_group()
inputs.add_argument("--input-dir", type=Path, help="maintenance18-ai944/와 se-ai-comparison/을 포함하는 입력 폴더 (기본값: data/inputs)")
inputs.add_argument("--raw5", type=Path, help="기존 RAW5 입력을 사용할 경우 지정하는 상위 폴더. 하위에 03_AI944개_전체_비교평가/comparison/이 있어야 합니다.")
parser.add_argument("--output-dir", type=Path, default=repo_root / "data", help="CSV 저장 폴더 (기본값: data). 같은 이름의 파일이 있으면 덮어씁니다.")
args = parser.parse_args()
if args.raw5:
    input_dir = args.raw5.expanduser().resolve() / "03_AI944개_전체_비교평가" / "comparison"
else:
    input_dir = (args.input_dir or repo_root / "data" / "inputs").expanduser().resolve()
data_dir = str(args.output_dir.expanduser().resolve())
os.makedirs(data_dir, exist_ok=True)

# 1. comparison.json에서 과제 번호별 벤치마크 종류를 읽는다.
comp_file = input_dir / "maintenance18-ai944" / "comparison.json"
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

raw_tasks_dir = input_dir / "se-ai-comparison" / "tasks"
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
    
    # 원본 데이터의 이슈 분류를 추출한다.
    # 1. PolyBench: task_category의 단일 분류를 사용한다.
    # 2. SWE-bench Pro: issue_specificity의 분류 목록을 사용한다.
    # 3. SWE-EVO: 두 항목이 없으면 unknown으로 기록한다.
    # 여러 분류가 있으면 목록 전체를 보존하고 첫 항목을 대표 분류로 사용한다.
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

# 2. 추출한 과제별 기본 정보를 baseline_tasks.csv에 저장한다.
baseline_csv = os.path.join(data_dir, "baseline_tasks.csv")
with open(baseline_csv, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(baseline_tasks[0].keys()))
    writer.writeheader()
    writer.writerows(baseline_tasks)

print(f"생성한 파일: {baseline_csv}")
print(f"복수 분류를 보존한 과제 수: {multilabel_count} (기존 분석 기록: Pro 731개 중 576개)")

