# 프로젝트 디렉터리 경계

프로젝트 전체 자료 위치는 [전체 디렉터리 안내](../docs/DIRECTORY_LAYOUT.md)를 따른다. 이 문서의 경로는 `new_project/` 기준이다. 현재 내부용 프로그램이며 아래 패키징 영역은 내부 PC 설치 묶음을 만드는 도구다.

## 사용자가 실행하는 제품 영역

- `src/govoffice/`: 실제 업무 기능과 한글 자동화 코드
- `assets/`: 아이콘과 제품 자원
- `config/`: 제품 레이아웃과 개발 실행용 데이터
- `runtime/`: 프로그램이 실행할 때 쓰는 자원
- `product/support/`: 사용자 PC에서 실행되는 설치·한글·보안 모듈 진단
- 최상위 `launch_*.ps1`, `*.cmd`, `gui_backend.py`, `*_ui.ps1`: 제품 진입점과 GUI

## 개발자만 사용하는 영역

- `development/tests/`: 자동검사와 WPF 검사 스크립트
- `development/tools/`: 복구, 추출, 실사 검증, 배포후 확인 도구
- `development/reports/`: 검증 결과와 실행 로그
- `development/docs/`: 개발 설계와 기능 문서
- `development/examples/`: 검증용 예시 문서
- `development/screenshots/`: GUI 비교·검증 이미지
- `development/run_tests.py`: 전체 검사 진입점

문서 목록은 [개발 문서 색인](development/docs/README.md)에서 확인한다. 제목·디자인 표 보호, 출력 서식 보정, 검토 메모, 양식 구조 저장 설계도 `development/docs/`로 통일했다.

## 배포를 만드는 영역

- `packaging/build_internal_release.py`: 배포 파일 허용 목록을 기준으로 ZIP 생성
- `packaging/installer/`: 사용자용 설치 스크립트와 안내
- `packaging/releases/`: 생성된 배포 산출물. Git 관리 대상에서 제외

분리 전에 생성해 개발용 Python 자료가 섞인 예전 배포판은 `packaging/releases/legacy_mixed_runtime/`에 보관한다. 새 배포는 해당 폴더를 사용하지 않는다.

`packaging/build_internal_release.py`는 `development/`를 배포하지 않는다. 사용자 배포판에는 제품 코드·자원·진단 도구만 들어간다. 또한 분석용 Python에 포함된 IDE, 예제, 테스트, 헤더와 빌드 도구는 배포 시 제외한다.
