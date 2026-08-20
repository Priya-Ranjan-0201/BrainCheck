@echo off
echo ==============================================
echo   Starting BrainCheck Quiz App (Local Mode)
echo ==============================================

IF NOT EXIST ".venv\" (
    echo Creating virtual environment...
    python -m venv .venv
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt

echo Starting Flask server...
flask run
