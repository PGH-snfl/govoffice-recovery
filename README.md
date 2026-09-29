# 범정부오피스

원본 범피스 기능 복구를 바탕으로 한글 문서 작업과 기관별 기능을 확장하는 **내부용 프로그램**이다.

실행하려면 [범정부오피스_실행.cmd](범정부오피스_실행.cmd)를 더블클릭한다. 원본 프로그램은 `originals/`에 보존하고 현재 실행 코드와 구분한다.

**처음 내려받았다면:** 저장소 전체 압축 해제 → [시작전_점검.cmd](시작전_점검.cmd) → [범정부오피스_실행.cmd](범정부오피스_실행.cmd). Windows 64비트와 설치된 데스크톱 한글이 필요하다. Python 3.13과 연결 라이브러리는 저장소에 포함돼 있다. 인공지능 작성은 별도 사용자 계정 연결이 필요한 선택 기능이다.

[처음 실행·개발 이어가기](docs/GETTING_STARTED.md) · [최종 점검 범위와 제한](docs/HANDOFF_2026-09-29.md)

## 폴더 한눈에 보기

```text
범정부오피스/
├─ 범정부오피스_실행.cmd  현재 프로그램 실행
├─ new_project/          실행 코드·개발 도구·사용자 데이터
├─ docs/                 전체 구조·작성 기준·작업 기록
├─ materials/            예시·제출서류·첨부·문서 검증 결과
├─ originals/            원본 실행파일·가이드
├─ exa-results/          레퍼런스 원문과 조사 기록
├─ recovered/            원본 기능의 복구 소스
├─ 범피스1303_분석/       추출·역컴파일 근거와 Python 실행환경
├─ recovery_analysis/    모듈별 복구 분석
├─ tools/                추출·복구 도구
├─ runtime/              한글 보안 모듈
├─ system_backups/       로컬 복구 백업·이동 기록
└─ tmp/                  임시 작업
```

[상세 구조와 이동 전후 경로](docs/DIRECTORY_LAYOUT.md) · [전체 문서 색인](docs/README.md)

## 무엇을 찾고 있나요?

| 목적 | 위치 |
|---|---|
| 현재 프로그램 설명 | [new_project/README.md](new_project/README.md) |
| 실제 기능 코드 | [new_project/src/govoffice/](new_project/src/govoffice/) |
| 개발 설계 문서 | [개발 문서 색인](new_project/development/docs/README.md) |
| 자동검사·검증 기록 | [tests](new_project/development/tests/) · [reports](new_project/development/reports/) |
| 사용자 문서와 참고자료 | [materials/README.md](materials/README.md) |
| 범피스 예시1·2 | [예시1](<materials/examples/범피스 예시1.hwp>) · [예시2](<materials/examples/범피스 예시2.hwp>) |
| 원본 실행파일·가이드 | [originals/README.md](originals/README.md) |
| 연구개발 문서 작성 기준 | [본문 작성 기억](docs/AUTHORING_REFERENCE_MEMORY.md) · [참고자료 삽입 기준](docs/AUTHORING_REFERENCE_INSERTION_STANDARD.md) |
| 레퍼런스 조사 | [90건 시각자료 색인](exa-results/reference-visuals-2026-09-25/README.md) |
| 복구 경위 | [복구 현황](recovered/복구현황.md) · [전체 개발 과정](docs/범정부오피스_개발전과정_20260929.md) |
| 임시파일 삭제·복구 | [정리 기록](docs/CLEANUP_2026-09-29.md) |

## 개발 영역 구분

- `new_project/`: 현재 프로그램의 기능 개발. `src/govoffice/` 아래 업무 기능·화면·기관별 기능·한글 연결을 나눠 관리한다.
- `recovered/`: 원본 동작을 보존하는 복구 소스. 현재 프로그램의 신규 업무 설계와 섞지 않는다.
- `범피스1303_분석/`, `recovery_analysis/`: 원본 근거·분석 자료. 임시 캐시처럼 일괄 삭제하지 않는다.
- `docs/`, `exa-results/`: 작성 기준과 조사 근거. 기억 저장과 실제 자동작성 기능 연결은 구분한다.

현재 프로그램은 검증 복구 소스를 `new_project/src/govoffice/runtime/recovered_hwp/`에서 사용한다. 연결 경계는 [코드 경계](docs/CODE_BOUNDARIES.md)를 참고한다.

## 검사 실행

프로젝트 루트에서:

```powershell
.\범피스1303_분석\python313\python.exe -B new_project\development\run_tests.py
```

실제 한글 연결·문서 편집 시험은 별도의 검증이며 사용자 원본 대신 사본으로 수행한다. 폴더 정리나 자동검사 일부 통과만으로 전 기능 검증 완료라고 판단하지 않는다.

## 보존과 Git 관리

원본 문서·복구 근거·사용자 저장값은 임의로 삭제하지 않는다. `tmp/`, `system_backups/`, 개인정보·즐겨찾기·프리셋·문서작성 작업 데이터는 해당 Git 제외 규칙을 따른다. 실제 한글·PDF 참고자료에는 개인정보 또는 대용량 파일이 있을 수 있으므로 업로드 전 개별 포함 여부를 확인한다.

2026-09-29 자료 폴더를 정리하고 현재 실행·연구 기억 경로는 보존했다. 과거 분석 로그의 경로는 당시 출처 기록이며, 현재 파일 위치는 [디렉터리 안내](docs/DIRECTORY_LAYOUT.md)를 기준으로 한다.
