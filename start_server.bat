@echo off
REM KoloCloud Server Startup Script for Windows

echo Starting KoloCloud Server...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r backend\requirements.txt

REM Check if .env file exists
if not exist "config\.env" (
    echo Warning: config\.env not found. Using default configuration.
    echo Please copy config\.env.example to config\.env and configure it.
)

REM Create necessary directories
if not exist "data\users" mkdir data\users
if not exist "data\temp" mkdir data\temp
if not exist "data\logs" mkdir data\logs

REM Set environment variables
set FLASK_APP=backend\app.py
set PYTHONPATH=%PYTHONPATH%;%cd%

REM Run the server
echo Starting server on http://localhost:5000
echo Press Ctrl+C to stop the server
python backend\app.py

pause
