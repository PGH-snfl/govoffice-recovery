# 전체 디렉터리 안내

정리일: 2026-09-29. 범정부오피스는 내부용 프로그램이다. 이번 작업은 파일 위치와 탐색 안내 정리이며 기능 구현·사용자 저장값 변경·GitHub 업로드가 아니다.

## 최상위 구조

```text
범정부오피스/
├─ 범정부오피스_실행.cmd       현재 프로그램 실행
├─ README.md                  프로젝트 시작 안내
├─ AGENTS.md                  작업 및 기억 파일 참조 규칙
├─ new_project/               현재 내부용 프로그램
│  ├─ src/govoffice/          실제 기능 코드
│  ├─ assets/                 화면 자원
│  ├─ config/                 레이아웃·사용자 데이터(위치 유지)
│  ├─ runtime/                실행 자원
│  ├─ ai_response_library/    저장된 작성 응답
│  ├─ product/support/        사용자 PC 진단
│  ├─ development/            tests·tools·reports·docs·examples 등
│  └─ packaging/              내부 설치 묶음 제작 도구
├─ docs/                      전체 구조·작성 기준·작업 기록
├─ materials/                 사용자 문서와 참고자료
│  ├─ examples/               범피스 예시1·2, 서식 보정 예시
│  ├─ submission-reference/   제출서류·매뉴얼·사업 참고자료
│  ├─ attachments/            기타 첨부자료
│  └─ validation/             실검증 양식·작성 결과
├─ originals/                 원본 실행파일·가이드
├─ exa-results/               레퍼런스 원문·조사 기록·조사 스크립트
├─ recovered/                 원본 기능을 보존하는 복구 소스
├─ 범피스1303_분석/            추출 근거·분석용 Python
├─ recovery_analysis/         모듈별 복구 분석
├─ tools/                     원본 추출·복구 도구
├─ runtime/                   공통 한글 보안 모듈
├─ system_backups/            로컬 복구 백업·이동 기록(Git 제외)
└─ tmp/                       임시 작업 영역(Git 제외)
```

## 실행과 검증

탐색기에서 루트의 `범정부오피스_실행.cmd`를 실행한다. 기존 `new_project/범정부오피스_실행.cmd`도 유지하며 같은 실행 경로다. 이번 정리 과정에서는 프로그램 창이나 한글 문서를 임의로 열지 않았다.

프로젝트 루트에서 자동검사:

```powershell
.\범피스1303_분석\python313\python.exe -B new_project\development\run_tests.py
```

`-B`는 Python 실행 캐시를 새로 만들지 않는 옵션이다. 전체 검사에는 이 PC의 환경에 의존하는 항목이 있을 수 있다. 이번 정리의 실제 검사 범위는 아래 검증 항목을 참고한다.

## 이동한 위치

| 이전 | 현재 |
|---|---|
| `범피스1303.exe`, `범피스가이드북.pdf` | `originals/` 아래 같은 파일명 |
| 루트 `범피스 예시1.hwp`, `범피스 예시2.hwp` | `materials/examples/` 아래 같은 파일명 |
| `예시 문서/` | `materials/examples/` |
| `3. 제출서류 및 참고/` | `materials/submission-reference/` |
| `첨부자료/` | `materials/attachments/` |
| `AI 문서 작성 실검증 결과/` | `materials/validation/` |
| `new_project/development/`의 설계 문서 4개 | `new_project/development/docs/` |

설계 문서 4개는 `DESIGN_TABLE_PROTECTION.md`, `OUTPUT_POLISH.md`, `REVIEW_MEMOS.md`, `TEMPLATE_LAYOUT_DATABASE.md`다. 파일명과 내용을 유지했다.

## 위치를 유지한 이유

- `new_project`, `recovered`, `범피스1303_분석`, `recovery_analysis`, `tools`, `runtime`은 실행·복구 도구가 사용하는 경로다. 폴더 이름을 일괄 변경하여 의존 관계를 바꾸지 않았다.
- `docs/AUTHORING_*.md`와 사례별 기억 파일은 작업 규칙이 직접 참조한다. `exa-results`도 조사 문서의 많은 상대 링크와 연결돼 있으므로 유지한다.
- `new_project/config`, 응답 라이브러리, 이미 등록된 양식·작업 이력은 유지했다. 사용자 데이터와 과거 출처 기록을 일괄 문자열 치환하지 않았다.
- 문서 이동 전 경로가 운영체제의 최근 파일 목록이나 외부 바로가기에 남아 있으면 새 위치에서 다시 선택해야 한다.

## 이동 및 검증 기록

12개 경로 묶음, 총 72개 파일을 이동했다. 이동 전후 모든 파일의 SHA-256(내용 동일 여부를 확인하는 해시값)이 일치했다. 삭제나 중복 파일 덮어쓰기는 하지 않았다.

이동 기록은 `system_backups/directory-layout-20260929-180239-580/manifest.json`에 있다. 각 파일의 이전·이후 상대경로와 해시값을 기록했다. 원래 위치로 되돌릴 때는 이 기록을 사용하고, 새로 생성된 파일을 덮어쓰지 않도록 확인한다.

기후부 양식 추출·자산 준비 도구 2개의 입력 경로를 새 위치로 변경했다. 기존 데이터·원문·문서 내용은 수정하지 않았다. 과거 청소 기록의 대용량 파일은 현재 `materials/validation/양식/`에 있다.

정리 후 구조·새 안내 링크·필수 실행 경로·입력 양식 위치·기능 카탈로그·연결 없는 런처 검사 12개가 통과했다. 최종 파일 해시 재검사도 72개 모두 일치했다. `organize_workspace.ps1`을 다시 미리보기로 실행한 결과 남은 이동 0개다. 실제 한글 문서 열기나 전체 기능 시험은 이번 정리 범위에 포함하지 않았다.

## 앞으로 저장할 위치

코드는 `new_project/src`, 개발 도구는 `new_project/development/tools`, 설계 문서는 `new_project/development/docs`, 실행 검증 기록은 `new_project/development/reports`에 둔다. 사용자 문서는 `materials`의 목적별 폴더로 구분한다. 원본 근거는 `originals`, 연구 레퍼런스는 `exa-results`, 단기 출력 미리보기는 `tmp`에 둔다.

GitHub 업로드 전에는 실제 문서의 개인정보와 대용량 파일 포함 여부를 별도로 확인한다. 디렉터리 정리 완료와 업로드 준비 완료는 같은 의미가 아니다.
