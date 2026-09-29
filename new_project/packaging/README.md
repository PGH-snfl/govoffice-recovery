# 배포 제작 영역

- `build_internal_release.py`: 제품 파일만 허용 목록으로 복사해 배포 ZIP을 만든다.
- `installer/`: 배포 ZIP 최상위에 들어갈 설치 파일이다.
- `releases/`: 생성된 결과물이다. `legacy_mixed_runtime/`은 디렉터리 분리 전에 만든 이전 배포판이며 재배포하지 않는다.

현재 배포판은 `development/`를 포함하지 않고, PyWin32의 IDE·예제·테스트·빌드 자료도 제외한다.
