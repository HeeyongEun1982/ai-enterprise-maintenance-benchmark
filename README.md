# Enterprise Maintenance Requirements × AI Coding Benchmark Evaluation

Research materials for the manuscript **“Beyond Task Complexity: Mapping Enterprise Maintenance Requirements to AI Coding Benchmark Evaluation”** (submitted for review at BenchSOC 2026). This repository is a **frozen analysis and partial verification package**, **not** an executable re-run of complete AI benchmark containers and not an independent annotation-reliability study.

## Study scope

- Enterprise corpus: **2,925** Apache Fineract resolved issues, decomposed into **3,811** requirement units. The full raw Jira issue export is **not** included in this public candidate; summarized annotations and selected traceability excerpts are provided.
- Benchmarks: **944** AI coding tasks: SWE-bench Pro **v1 (731 tasks)**, PolyBench Java **165**, SWE-EVO **48**. The SWE-bench Pro default dataset changed to V2 in September 2026; the 731-task study uses **v1**, not today's default. See [original v1 dataset](https://huggingface.co/datasets/ScaleAI/SWE-bench_Pro).
- **3,446** task–criterion assignments against the frozen 18-criterion A/B taxonomy (six maintenance activities and twelve fulfillment conditions).
- E1: **1,177** matching pairs, mean Jaccard distance **0.8138** and **676** fully disjoint pairs. Matching controls native issue type and number of changed files exactly, and patch churn within a tolerance. This is not matched difficulty.
- E2: Corpus co-occurrence (e.g. Fineract B4–B2 phi ~**+0.430**, AI phi ~**−0.013**), **16** source-grounded business dependency relationships plus one technical reference, and four illustrative benchmark-oracle case studies. Co-occurrence is not causality and examples are not prevalence estimates.

## Start here

```bash
python -m pip install -r requirements.txt
python scripts/verify_all_claims.py
```

This runs **six targeted numerical/structural checks** over the included CSVs and evidence exports. Passing these checks does **not** establish semantic annotation validity, independent inter-annotator reliability, completeness of external evaluation harnesses, or license clearance.

For deeper checks with data already present:

```bash
python scripts/08_verify_gate2_master_plan.py
python scripts/09_verify_gate3.py
python ablation_study/nodebb_0030/inspect_nodebb_oracle.py
```

The NodeBB script examines the provided reference/ablated patches and the **supplied F2P test patch statically**. It does **not** run a benchmark container, measure a pass rate, or prove that other tests in the complete harness cannot detect migration errors. The developer migration file adds **44 LOC** and spans a **50-line unified-diff hunk**; these are not equivalent lengths.

### Re-generating selected outputs

The following use inputs **included here** (prefer a fresh clone or backup; generators overwrite their output files):

```bash
python scripts/03_generate_e1_matched_pairs.py
python scripts/04_generate_gate1_statistics.py
python scripts/09_generate_gate3_artifacts.py
```

`01_generate_baseline_tasks.py` and `02_generate_ab_long.py` require separately obtained original **RAW5** upstream inputs (`--raw5 PATH`). These RAW5 sources are **not packaged**, so those two generators are **not self-contained**. For example:

```bash
python scripts/01_generate_baseline_tasks.py --help
python scripts/02_generate_ab_long.py --help
```

`06_reviewer_rebuttal_metrics.py` uses included summaries, but any core-versus-infrastructure subdivision requiring the original full Fineract issue text is unavailable in the release. `10_verify_gate4.py` is an optional manuscript-text check requiring a separate draft path via the `PAPER_DRAFT` environment variable; the submitted manuscript is not distributed here.

## Key files

| Path | Purpose |
|---|---|
| `data/framework-snapshot.json` | **Frozen 18-criterion codebook** (source of truth for names and boundaries) |
| `data/baseline_tasks.csv`, `data/ab_long.csv` | Task census, family metadata and coding decisions |
| `data/ab_all_evidences.csv` | Source quotations and coding rationales; not independently adjudicated labels |
| `data/e1_matched_pairs.csv` | E1 matching results |
| `data/gate3_*.csv` | Family tables, |B| distribution and pairwise phi values |
| `data/gate2_*.csv` | Selected dependency and test-assertion evidence |
| `data/fineract/summary.json`, `data/fineract/requirement-units.json` | Fineract summary and requirement-unit annotations |
| `data/fineract/gate2_raw_source_snippets.json` | Selected source-grounding excerpts, with original text/offsets |
| `data/ai_case_sources/` | Selected case specifications (third-party-origin text; see notices) |
| `ablation_study/nodebb_0030/` | NodeBB static patch-and-oracle comparison, **not a dynamic experiment** |
| `evidence/` | Reports and full evidence-table files; historical reports retain original paths and scope notes |
| `scripts/verify_all_claims.py` | Six numerical/structural checks (not a complete end-to-end regeneration) |

## The immutable codebook

The `name` field of `data/framework-snapshot.json` is authoritative; translations or paraphrases must **not** replace it in data exports. The B10–B12 labels are **service continuity/failure handling; interface/environment compatibility; user interaction**, not persistence retention, protocol conformance, or operational robustness.

| Code | Frozen original name |
|---|---|
| `A1` | 제품 동작·업무 규칙 |
| `A2` | 구조·구현 방식 |
| `A3` | 시험·품질 확인 |
| `A4` | 실행·운영 |
| `A5` | 배포·버전·환경 전환 |
| `A6` | 개발 절차·문서·프로젝트 지원 |
| `B1` | 기능 결과·입력 조건 |
| `B2` | 수치·계산 정확성 |
| `B3` | 데이터 관계·정합성 |
| `B4` | 시간·순서에 따른 의미 |
| `B5` | 상태·업무 흐름 |
| `B6` | 기존 정보·동작의 보존 |
| `B7` | 동시 실행·트랜잭션 경계 |
| `B8` | 권한·보호 |
| `B9` | 성능·자원 사용 |
| `B10` | 서비스 지속·실패 대응 |
| `B11` | 인터페이스·환경 호환 |
| `B12` | 사용자 상호작용 |

## Validity and transparency

A single primary investigator performed the semantic coding. There is **no substantiated blinded second coder or Cohen's kappa estimate** for this study. The earlier inter-annotator CSV and claimed κ figure were removed from this release because their independent collection/provenance was not established. The historical `evidence/STORYLINE_VERIFICATION_REPORT.md` also records this limitation. See [annotation protocol](data/ANNOTATION_PROTOCOL.md).

Automated citation, string-offset and consistency checks confirm only their respective mechanical properties; they are not semantic adjudication. The four qualitative oracle case studies use **static analysis of specified artifacts**, not executed benchmarks, full-harness coverage, or measured resolved rates. Selected illustrative cases cannot support population-wide oracle omission rates or claims about real-world production failure prevalence.

## Source provenance, privacy and licensing

This release removes `data/fineract/fineract_resolved_issues.json` because the full source issue export contains upstream copyrighted content and email addresses; detailed source provenance is available from the official Apache Fineract project. The remaining excerpt-bearing files also require human clearance before a **public GitHub push**.

See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) and [LICENSE.md](LICENSE.md). **No blanket CC BY or MIT relicensing of upstream benchmark texts, original repository patches, or Jira descriptions is asserted.** SWE-bench Pro's dataset card explicitly states task content retains individual source-repository licenses; NodeBB itself is GPL-3.0. Authorship, redistribution rights and required notices remain a human review item before publishing. Never commit credentials or personal information.

## Citation and paper status

Manuscript: *Beyond Task Complexity: Mapping Enterprise Maintenance Requirements to AI Coding Benchmark Evaluation* (BenchSOC 2026 submission). **Do not use an accepted-proceedings BibTeX entry unless and until acceptance/publication details are confirmed.** Cite original benchmark authors and dataset versions separately; see upstream dataset pages for authoritative references.
