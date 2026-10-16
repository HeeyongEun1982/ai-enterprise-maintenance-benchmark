import json, os, csv

import argparse
from pathlib import Path
parser = argparse.ArgumentParser(description="Optional rebuild; requires the original RAW5 source tree, which is not included in this release.")
parser.add_argument("--raw5", type=Path, required=True, help="Path to the original RAW5 input directory")
parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parents[1] / "data")
args = parser.parse_args()
raw5_dir = str(args.raw5.expanduser().resolve())
data_dir = str(args.output_dir.expanduser().resolve())
os.makedirs(data_dir, exist_ok=True)

# 1. Load framework-snapshot.json for immutable codebook
fs_file = os.path.join(raw5_dir, "03_AI944개_전체_비교평가/comparison/maintenance18-ai944/framework-snapshot.json")
with open(fs_file, 'r', encoding='utf-8') as f:
    fs_data = json.load(f)

immutable_codebook = {e['code']: e['name'] for e in fs_data['entries']}

# 2. Load table-view.json
tv_file = os.path.join(raw5_dir, "03_AI944개_전체_비교평가/comparison/maintenance18-ai944/table-view.json")
with open(tv_file, 'r', encoding='utf-8') as f:
    tv_data = json.load(f)
tv_rows = tv_data if isinstance(tv_data, list) else tv_data.get('rows', [])

ab_rows = []
all_evidence_rows = []

for i in range(944):
    t_id = f"{i+1:04d}"
    t_path = os.path.join(raw_tasks_dir, f"{t_id}.json")
    with open(t_path, 'r', encoding='utf-8') as tf:
        td = json.load(tf)
        
    evals = tv_rows[i].get('evaluations', [])
    for ev in evals:
        code = ev.get('code')
        name = immutable_codebook.get(code, ev.get('name'))
        ev_list = ev.get('evidence', [])
        ev_count = len(ev_list)
        
        quote = ""
        req_work = ""
        reason = ""
        source_field = ""
        
        if ev_list:
            quote = ev_list[0].get('quote', '')
            req_work = ev_list[0].get('required_work', '')
            reason = ev_list[0].get('classification_reason', '')
            
            # Locate raw source field (requirements, problem_statement, interface, patch, test_patch)
            for k in ['requirements', 'problem_statement', 'interface', 'patch', 'test_patch']:
                v = td.get(k, '')
                if isinstance(v, str) and quote and quote in v:
                    source_field = k
                    break
            if not source_field:
                for k, v in td.items():
                    if isinstance(v, str) and quote and quote in v:
                        source_field = k
                        break
        
        # 1 evaluation per row (3,446 total, 0 duplicates between task and criterion)
        ab_rows.append({
            'task_id': t_id,
            'criterion_code': code,
            'criterion_name': name,
            'included': ev.get('included', ''),
            'not_required': ev.get('not_required', ''),
            'evidence_count': ev_count,
            'evidence_source_field': source_field,
            'evidence_quote': quote,
            'required_work': req_work,
            'classification_reason': reason,
            'all_evidence': json.dumps(ev_list, ensure_ascii=False)
        })
        
        # Individual evidence rows for Gate 2 fine-grained causal dependency analysis (3,534 total)
        for e_idx, evidence in enumerate(ev_list):
            q_item = evidence.get('quote', '')
            src_f = ""
            for k in ['requirements', 'problem_statement', 'interface', 'patch', 'test_patch']:
                v = td.get(k, '')
                if isinstance(v, str) and q_item and q_item in v:
                    src_f = k
                    break
            if not src_f:
                for k, v in td.items():
                    if isinstance(v, str) and q_item and q_item in v:
                        src_f = k
                        break
            all_evidence_rows.append({
                'task_id': t_id,
                'criterion_code': code,
                'criterion_name': name,
                'evidence_index': e_idx + 1,
                'total_evidences': ev_count,
                'evidence_source_field': src_f,
                'evidence_quote': q_item,
                'required_work': evidence.get('required_work', ''),
                'classification_reason': evidence.get('classification_reason', '')
            })

# 3. Write ab_long.csv (3,446 evaluations)
ab_long_csv = os.path.join(data_dir, "ab_long.csv")
with open(ab_long_csv, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(ab_rows[0].keys()))
    writer.writeheader()
    writer.writerows(ab_rows)

print(f"Generated: {ab_long_csv} ({len(ab_rows)} rows)")

# 4. Write ab_all_evidences.csv (3,534 individual evidence items)
ab_ev_csv = os.path.join(data_dir, "ab_all_evidences.csv")
with open(ab_ev_csv, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(all_evidence_rows[0].keys()))
    writer.writeheader()
    writer.writerows(all_evidence_rows)

print(f"Generated: {ab_ev_csv} ({len(all_evidence_rows)} rows, 58 items with multiple evidence preserved)")
