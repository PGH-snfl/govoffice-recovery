# 범정부오피스 한 번에 실행하기

Windows 64비트와 설치된 데스크톱 한컴 한글이 필요합니다. 저장소 전체를 내려받은 뒤 루트에서 실행합니다.

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\run_govoffice.ps1
```

또는 `run_govoffice.cmd`를 더블클릭합니다. Git Bash에서는:

```bash
bash run_govoffice.sh
```

번들 Python으로 기존 `check_checkout.py` 사전 점검을 실행하고, 성공하면 기존 `new_project/launch_gui.ps1`을 엽니다. 기존 런처의 UAC 요청은 Windows에서 확인해야 합니다. 실행 정책 옵션은 이번 PowerShell 프로세스에만 적용됩니다.

## 점검과 경로 지정

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\run_govoffice.ps1 -CheckOnly
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\run_govoffice.ps1 -ProjectDir "C:\work\govoffice"
```

`-CheckOnly`는 준비·사전 점검까지만 수행하며 문서 편집을 하지 않습니다. 저장소 루트에서 실행하면 자기 폴더를 사용합니다. 실행기만 외부에 복사했다면 옆의 `govoffice-recovery/`를 기본 대상으로 사용하고, 그 폴더가 없으면 인증된 GitHub 계정으로 clone합니다. 기존 폴더는 자동 pull하지 않습니다.

- `run_govoffice.sh`는 Windows Git Bash용 진입점입니다. Ubuntu/macOS/WSL에서는 지원하지 않는 환경임을 알리고 종료합니다.
- Python 3.13과 연결 라이브러리는 저장소에 포함되어 있어 별도 Conda/pip 설치가 필요하지 않습니다. `new_project/`만 복사하면 필수 실행환경이 빠집니다.
- 웹 한글·뷰어만으로는 COM 자동화를 할 수 없습니다. 한글과 보안 모듈 비트수도 맞아야 합니다.
- 종료는 프로그램 창에서 문서 저장 여부를 확인한 뒤 진행합니다. 사용자 데이터와 기존 한글 프로세스를 일괄 삭제·종료하지 않습니다.
- AI 작성 계정 연결은 선택 기능이며 기본 한글 실행과 별도입니다.

## 검증 범위

2026-11-10: 기존 실행 경로와 점검기를 읽고 연결했으며 Bash 플랫폼 검사와 PowerShell UTF-8 BOM/CRLF를 확인했습니다. Ubuntu에서는 Windows PowerShell·WPF·한글 COM 실사를 할 수 없어 실제 Windows 실행과 문서 편집은 미검증입니다. 최초 사용은 예시 문서 사본으로 확인하세요.

[전체 시작 안내](docs/GETTING_STARTED.md) · [기존 인계 검증 범위](docs/HANDOFF_2026-09-29.md)
