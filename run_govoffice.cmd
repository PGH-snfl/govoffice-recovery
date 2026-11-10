@echo off
setlocal
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0run_govoffice.ps1" %*
set "RESULT=%errorlevel%"
if not "%RESULT%"=="0" pause
exit /b %RESULT%
