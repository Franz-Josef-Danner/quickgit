@echo off
setlocal
cd /d "%~dp0"

REM Startet die UI mit dem Python-Launcher im GUI-Modus (ohne Konsole)
pyw quickgit_ui.pyw

if errorlevel 1 (
  echo.
  echo Fehler: pyw konnte quickgit_ui.pyw nicht starten.
  echo Stelle sicher, dass Python korrekt installiert ist
  echo und die Option "Add python.exe to PATH" aktiv war.
  pause
)
