@echo off
setlocal
cd /d "%~dp0"
python --version >nul 2>&1
if errorlevel 1 (
  echo Python is not installed or not on PATH.
  pause
  exit /b 1
)
python check_ollama.py
if errorlevel 1 (
  echo Start Ollama and install at least one model before continuing.
  pause
  exit /b 1
)
echo.
echo Example: python batch_run.py --mode ollama --models llama3.2 --rounds 3
echo This script does not automatically download any models or make transactions.
pause
