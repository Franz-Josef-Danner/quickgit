@echo off
setlocal
cd /d "%~dp0"

REM 1) Bevorzugt Python Launcher ohne Konsole
where pyw >nul 2>&1
if %errorlevel%==0 (
  pyw quickgit_ui.pyw
  if %errorlevel%==0 goto :eof
)

REM 2) Fallback: pythonw.exe ohne Konsole
where pythonw >nul 2>&1
if %errorlevel%==0 (
  pythonw quickgit_ui.pyw
  if %errorlevel%==0 goto :eof
)

REM 3) Letzter Fallback: python.exe (mit Konsole)
where python >nul 2>&1
if %errorlevel%==0 (
  python quickgit_ui.pyw
  if %errorlevel%==0 goto :eof
)

echo.
echo Fehler: QuickGit UI konnte nicht gestartet werden.
echo Weder pyw, pythonw noch python wurden gefunden.
echo.
echo Loesung:
echo 1) Python installieren: https://www.python.org/downloads/windows/
echo 2) Bei Installation aktivieren:
echo    - Add python.exe to PATH
echo    - Install launcher for all users (recommended)
echo.
pause
