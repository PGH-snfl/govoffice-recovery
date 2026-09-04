# 프로젝트 디렉터리 구조

```text
범정부오피스/
├─ 범피스1303_분석/       실행 파일 원본 분석 증거
├─ recovery_analysis/     재생성 가능한 분석 자료
├─ recovered/             원본 동작과 API의 복구 저장소
│  ├─ 한컴오피스/recovered_source/
│  ├─ 한컴오피스/compat/
│  └─ metadata/
└─ new_project/           신규 범정부오피스 개발 영역
   ├─ src/govoffice/
   │  ├─ app/
   │  ├─ domain/
   │  ├─ ports/
   │  ├─ services/
   │  ├─ adapters/
   │  └─ institutions/
   └─ tests/
```

복구가 끝난 메서드만 `recovered_source/`에 저장한다. 미복구 메서드는
`compat/legacy_runtime.py`를 통하며, `metadata/hwp_coverage.json`에서
`bytecode_backed`로 표시한다. 신규 프로젝트는 복구 패키지를 직접 import하지
않고 `new_project/src/govoffice/adapters/`를 통해 접근한다.

