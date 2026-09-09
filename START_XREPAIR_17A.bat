@echo off
setlocal EnableExtensions
title X-Repair 17A
cd /d "%~dp0"

echo ==========================================================
echo                  X-REPAIR 17A
echo        Diagnostic vibratoire intelligent
echo ==========================================================
echo.

set "PY_CMD="
where py >nul 2>&1
if %errorlevel%==0 (
  set "PY_CMD=py -3"
) else (
  where python >nul 2>&1
  if %errorlevel%==0 set "PY_CMD=python"
)

if "%PY_CMD%"=="" (
  echo [ERREUR] Python 3 est introuvable.
  echo Installez Python 3.10+ puis cochez "Add Python to PATH".
  pause
  exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
  echo [1/4] Creation de l'environnement virtuel...
  %PY_CMD% -m venv .venv
  if errorlevel 1 goto :fail
)

call ".venv\Scripts\activate.bat"
if errorlevel 1 goto :fail

echo [2/4] Mise a jour de pip...
python -m pip install --upgrade pip
if errorlevel 1 goto :fail

echo [3/4] Installation / verification des dependances...
python -m pip install -r requirements.txt
if errorlevel 1 goto :fail

echo [4/4] Demarrage de l'interface...
python -m streamlit run app.py --server.headless false --browser.gatherUsageStats false
if errorlevel 1 goto :fail
exit /b 0

:fail
echo.
echo [ERREUR] Le demarrage a echoue.
pause
exit /b 1
