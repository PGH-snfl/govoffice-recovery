@echo off
setlocal
chcp 65001 >nul
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"
set "PROJECT_DIR=%~dp0"
set "WORKSPACE_DIR=%~dp0.."
set "PYTHON_EXE="
if exist "%PROJECT_DIR%runtime\python\python.exe" set "PYTHON_EXE=%PROJECT_DIR%runtime\python\python.exe"
if not defined PYTHON_EXE for /d %%D in ("%WORKSPACE_DIR%\*1303_*") do if exist "%%~fD\python313\python.exe" set "PYTHON_EXE=%%~fD\python313\python.exe"
if not defined PYTHON_EXE (
  echo Bundled Python was not found.
  pause
  exit /b 1
)
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%PROJECT_DIR%launch_gui.ps1"
if errorlevel 1 (
  echo Launcher exited with an error.
  pause
)
