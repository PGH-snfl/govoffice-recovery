# 복구 코드와 새 프로젝트의 경계

| 위치 | 역할 | 수정 원칙 |
|---|---|---|
| `범피스1303_분석/` | 실행 파일에서 추출한 marshal·디스어셈블 | 원본 증거이므로 읽기 전용 |
| `recovery_analysis/` | 복구 과정의 분석 자료 | 도구로 재생성 가능 |
| `recovered/` | 원본 API를 보존하는 복구 코드 | 바이트코드 근거가 있는 복구만 반영 |
| `new_project/` | 앞으로 개발할 새 범정부오피스 | 업무 설계와 신규 기능만 반영 |

새 프로젝트는 복구 패키지를 직접 참조하지 않는다. 연결이 필요할 때는
`new_project/src/govoffice/adapters/recovered_hwp.py`를 통한다. 이 규칙은
`new_project/development/tests/test_architecture.py`에서 자동 검사한다.
