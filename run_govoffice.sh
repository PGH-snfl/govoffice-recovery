#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if [[ "${1:-}" == --help || "${1:-}" == -h ]]; then
  cat <<'EOF'
Windows Git Bash: bash run_govoffice.sh [-ProjectDir 'C:\work\govoffice'] [-CheckOnly]
Windows PowerShell: powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\run_govoffice.ps1
Windows 64비트 + 설치된 데스크톱 한글이 필요합니다. Ubuntu/macOS에서는 실행할 수 없습니다.
-CheckOnly는 준비·점검까지만 수행합니다. 기존 문서를 열지 않습니다.
EOF
  exit 0
fi
case "$(uname -s)" in
  MINGW*|MSYS*|CYGWIN*)
    command -v powershell.exe >/dev/null || { echo 'Windows PowerShell 5.1을 찾지 못했습니다.' >&2; exit 1; }
    SCRIPT_WIN="$(cygpath -w "$SCRIPT_DIR/run_govoffice.ps1")"
    export MSYS2_ARG_CONV_EXCL='*'
    exec powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$SCRIPT_WIN" "$@"
    ;;
  *)
    printf '%s\n' '범정부오피스는 Windows WPF·한글 COM 프로그램입니다.' '이 Ubuntu/macOS/WSL 셸에서는 실행하지 않습니다. Windows PC에 묶음을 복사하고 run_govoffice.ps1을 실행하세요.' >&2
    exit 2
    ;;
esac
