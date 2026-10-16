#!/usr/bin/env python3
"""Source-grounded condition CO-PRESENCE summary, not causal/dependency coding.

Usage from repository root: python scripts/11_multi_condition_comparison.py
Inputs: data/fineract/requirement-units.json, data/framework-snapshot.json,
        data/baseline_tasks.csv, data/ab_long.csv
Output: data/gate5_multi_condition_summary.csv
Does not overwrite original Gate 1-4 results.
"""
from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

from scipy.stats import fisher_exact
from statsmodels.stats.contingency_tables import Table2x2
from statsmodels.stats.proportion import proportion_confint

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'


def issue_sets():
    snapshot = json.loads((DATA / 'framework-snapshot.json').read_text(encoding='utf-8'))
    issues = {entry['issue']: set() for entry in snapshot['issue_register']}
    units = json.loads((DATA / 'fineract' / 'requirement-units.json').read_text(encoding='utf-8'))
    for unit in units:
        issue = unit['issue']
        if issue not in issues:
            raise ValueError(f'Unexpected issue {issue}')
        for obj in unit['properties']:
            code = obj if isinstance(obj, str) else obj['code']
            if code.startswith('B'):
                issues[issue].add(code)
    assert len(issues) == 2925
    return issues


def benchmark_sets():
    with (DATA / 'baseline_tasks.csv').open(newline='',encoding='utf-8-sig') as f:
        entries = list(csv.DictReader(f))
    tasks = {int(x['task_id']): set() for x in entries}
    families = {int(x['task_id']): x['benchmark_family'] for x in entries}
    with (DATA / 'ab_long.csv').open(newline='',encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            key = int(row['task_id'])
            if key not in tasks:
                raise ValueError(f'Unknown benchmark task {key}')
            if row['criterion_code'].startswith('B'):
                tasks[key].add(row['criterion_code'])
    assert len(tasks) == 944
    return tasks, families


def aggregate(name, sets):
    n = len(sets)
    has = lambda x,*codes: all(c in x for c in codes)
    b4 = sum(has(x,'B4') for x in sets)
    b2 = sum(has(x,'B2') for x in sets)
    b4b2 = sum(has(x,'B4','B2') for x in sets)
    triple_b3 = sum(has(x,'B4','B2','B3') for x in sets)
    triple_b6 = sum(has(x,'B4','B2','B6') for x in sets)
    b4b2_b3or6 = sum(has(x,'B4','B2') and ('B3' in x or 'B6' in x) for x in sets)
    lower, upper = proportion_confint(b4b2,b4,method='wilson') if b4 else (float('nan'),float('nan'))
    return dict(corpus=name,N=n,B4=b4,B2=b2,B4_and_B2=b4b2,
                P_B2_given_B4=b4b2/b4 if b4 else float('nan'),
                P_B2_given_B4_wilson_lo=lower,P_B2_given_B4_wilson_hi=upper,
                B4_B2_B3=triple_b3,B4_B2_B6=triple_b6,
                B4_B2_B3_or_B6=b4b2_b3or6,
                P_B4_B2_B3_or_B6=b4b2_b3or6/n)


def main():
    fine = issue_sets()
    bench,family = benchmark_sets()
    rows = [aggregate('Apache Fineract',list(fine.values())),
            aggregate('AI pooled',list(bench.values()))]
    for fam in ('SWE-bench Pro','PolyBench Java','SWE-EVO'):
        rows.append(aggregate(fam,[value for i,value in bench.items() if family[i]==fam]))
    assert (rows[0]['B4'],rows[0]['B2'],rows[0]['B4_and_B2'])==(520,452,254)
    assert (rows[1]['B4'],rows[1]['B2'],rows[1]['B4_and_B2'])==(86,65,5)
    tab=[[254,520-254],[5,86-5]]
    fisher_p=fisher_exact(tab).pvalue
    rr=Table2x2(tab)
    out=DATA/'gate5_multi_condition_summary.csv'
    with out.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    for row in rows:
        print(f"{row['corpus']:<17} N={row['N']:>4}, B4={row['B4']:>3}, B4&B2={row['B4_and_B2']:>3}, "
              f"P(B2|B4)={100*row['P_B2_given_B4']:.2f}%, B4&B2&(B3|B6)={row['B4_B2_B3_or_B6']}")
    print(f'Fineract vs AI pooled conditional RR={rr.riskratio:.3f} (95% CI {rr.riskratio_confint()[0]:.3f}–{rr.riskratio_confint()[1]:.3f})')
    print(f'Fisher exact (B2 given B4; descriptive cross-corpus contrast) p={fisher_p:.6g}')
    print('CAUTION: All comparisons are cross-domain and describe co-presence, NOT directional dependencies.')
    print(f'Wrote {out}')

if __name__=='__main__':main()
