@echo off
cd .\Program
echo Instalowanie wymaganych bibliotek z setup.py...
pip install .

echo.
echo Uruchamianie programu Python...
python main.py

pause
