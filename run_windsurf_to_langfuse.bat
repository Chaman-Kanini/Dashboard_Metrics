@echo off
echo ============================================================
echo Windsurf Logs to Langfuse Integration
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

REM Check if dependencies are installed
echo Checking dependencies...
pip show langfuse >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo.
echo Running script...
echo.

REM Run the Python script
python windsurf_to_langfuse.py

echo.
echo ============================================================
echo Script execution completed
echo ============================================================
pause
