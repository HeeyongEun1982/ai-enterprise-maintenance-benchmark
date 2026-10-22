# 02_generate_ab_long.py 입력 자료

이 폴더에는 02번 소스가 사용하는 입력을 별도로 모았습니다.

| 파일 | 역할 |
|---|---|
| `framework-snapshot.json` | 원본 분류 코드와 명칭 |
| `table-view.json` | 과제별 A/B 평가와 근거 인용 |
| `tasks/0001.json` ~ `0944.json` | 인용문 출처를 찾는 과제 원문 944개 |
| `PROVENANCE.json` | 원본 위치·파일 크기·SHA-256 복사 검증 기록 |

원본은 작업 폴더의 `comparison/maintenance18-ai944/` 및
`comparison/se-ai-comparison/tasks/`에서 내용 변경 없이 복사했습니다.
기존 `data/framework-snapshot.json`은 덮어쓰지 않았습니다.

소스는 자신의 위치를 기준으로 `../data/02_generate_ab_long/`을 읽습니다.
실행하는 터미널의 현재 폴더에 따라 입력 위치가 바뀌지 않습니다.

공개 패키지의 루트에서 다음과 같이 실행하면 기존 CSV를 보존하면서 확인할 수 있습니다.

```bash
python scripts/02_generate_ab_long.py --output-dir ab-check
```

`--output-dir`를 생략하면 기존처럼 `data/`에 CSV를 저장하며, 같은 이름의 파일을 덮어씁니다.
다른 입력 폴더를 지정하려면 `--input-dir`를 사용합니다. 기존 `--raw5` 옵션도 유지했습니다.

2026-10-21 재생성 결과, `ab_long.csv` 3,446행과 `ab_all_evidences.csv` 3,534행의
모든 항목 값이 기존 공개 CSV와 일치했습니다. 원본과 복사본 946개의 해시도 모두 일치했습니다.
