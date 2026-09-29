@echo off
setlocal
chcp 65001 >nul
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"
set "PYTHONDONTWRITEBYTECODE=1"
set "CHECKOUT_PYTHON="
for /d %%D in ("%~dp0*1303_*") do if exist "%%~fD\python313\python.exe" set "CHECKOUT_PYTHON=%%~fD\python313\python.exe"
if not defined CHECKOUT_PYTHON (
  echo Bundled Python is missing. Extract the entire repository first.
  pause
  exit /b 1
)
"%CHECKOUT_PYTHON%" -B "%~dp0new_project\development\run_tests.py"
set "CHECK_RESULT=%errorlevel%"
pause
exit /b %CHECK_RESULT%
