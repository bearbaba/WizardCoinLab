@echo off
cd /d "%~dp0"
python -m unittest discover -s tests -v
if errorlevel 1 (echo Test failed & pause & exit /b 1)
python wizard_lab.py --mode mock --mock-kind reject --rounds 3
pause
