# 범피스 원본 복구 코드

이 디렉터리는 `범피스1303.exe`에서 추출한 Python 3.13 바이트코드의
복구 결과만 보관한다. 신규 제품 개발 코드는 상위 `new_project/`에 둔다.

## 저장 규칙

```text
recovered/
├─ 한컴오피스/
│  ├─ recovered_source/       일반 Python 소스로 복구 완료
│  │  ├─ common/              연결·명령·서식·문서·표·텍스트 등
│  │  └─ generated/           디스어셈블에서 자동 소스화
│  │     ├─ common/
│  │     ├─ hwp1/
│  │     ├─ hwp2/
│  │     └─ main/
│  ├─ compat/                 아직 미복구인 바이트코드 런타임
│  ├─ facades/                공개 API 재노출
│  └─ 한컴라이브러리*.py      원본 import 경로 호환
├─ metadata/                  API manifest와 메서드별 복구 상태
└─ tests/                     API·동작·경계 검사
```

`recovered_source/`에서는 `marshal`과 `compat`를 참조할 수 없다.
`compat/`에는 `legacy_runtime.py` 이외의 기능 구현을 두지 않는다.
이 규칙은 `tests/test_hwp_boundaries.py`가 검사한다.

## 현재 한글 복구 상태

- 전체 공개 API: 1,511개
- 일반 Python 소스: 1,353개
- 미복구 바이트코드 호환: 100개
- 누락 및 시그니처 불일치: 0개
