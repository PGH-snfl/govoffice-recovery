# 한글 복구 상태 메타데이터

- `hwp_api_manifest.json`: 원본 공개 API의 이름과 시그니처
- `hwp_coverage.json`: 각 API의 `source_recovered` 또는 `bytecode_backed` 상태

`source_recovered`는 `한컴오피스/recovered_source/`의 일반 Python 구현을
사용한다. `bytecode_backed`는 아직 복구되지 않았으며
`한컴오피스/compat/legacy_runtime.py`를 통해서만 실행된다.

