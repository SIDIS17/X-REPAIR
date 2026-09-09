@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title X-Repair 17A

echo ============================================================
echo                    X-REPAIR 17A
echo         Vibe Circuit Acoustic Thermal Power Core
echo ============================================================
echo.

set "PY="
where py >nul 2>&1 && set "PY=py -3"
if "%PY%"=="" (
  where python >nul 2>&1 && set "PY=python"
)
if "%PY%"=="" (
  echo [ERREUR] Python 3 introuvable.
  echo Installez Python 3.10+ et cochez Add Python to PATH.
  pause
  exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
  echo [1/3] Creation environnement virtuel...
  %PY% -m venv .venv
  if errorlevel 1 goto :fail
)

call ".venv\Scripts\activate.bat"
echo [2/3] Installation dependances...
python -m pip install --upgrade pip >nul
python -m pip install -r requirements.txt
if errorlevel 1 goto :fail

echo [3/3] Demarrage...
start "" http://127.0.0.1:8000
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
exit /b 0

:fail
echo Echec du demarrage.
pause
exit /b 1
