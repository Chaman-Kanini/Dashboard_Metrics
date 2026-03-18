@echo off
echo ======================================================================
echo IDE Logs Dashboard - Setup and Test Script
echo ======================================================================
echo.

echo Step 1: Checking Prerequisites...
echo.

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.8+
    pause
    exit /b 1
)
echo [OK] Python found

where dotnet >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] .NET SDK not found. Please install .NET 8 SDK
    pause
    exit /b 1
)
echo [OK] .NET SDK found

where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Node.js not found. Please install Node.js 18+
    pause
    exit /b 1
)
echo [OK] Node.js found

where psql >nul 2>nul
if %errorlevel% neq 0 (
    echo [WARNING] PostgreSQL psql not found in PATH
    echo Please ensure PostgreSQL is installed and running
) else (
    echo [OK] PostgreSQL found
)

echo.
echo Step 2: Installing Python Dependencies...
echo.
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install Python dependencies
    pause
    exit /b 1
)
echo [OK] Python dependencies installed

echo.
echo Step 3: Testing Database Connection...
echo.
python -c "import psycopg2; from dotenv import load_dotenv; import os; load_dotenv(); conn = psycopg2.connect(host=os.getenv('DB_HOST'), port=os.getenv('DB_PORT'), database=os.getenv('DB_NAME'), user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD')); print('[OK] Database connected'); conn.close()"
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Database connection failed!
    echo.
    echo Please ensure:
    echo 1. PostgreSQL is running
    echo 2. Database 'ide_logs' exists
    echo 3. Password in .env is correct
    echo 4. Run: psql -U postgres -d ide_logs -f database\schema.sql
    echo.
    pause
    exit /b 1
)

echo.
echo Step 4: Running Log Scraper...
echo.
python windsurf_to_langfuse.py
if %errorlevel% neq 0 (
    echo [WARNING] Log scraper encountered errors
    echo Check the output above for details
)

echo.
echo ======================================================================
echo Setup Complete!
echo ======================================================================
echo.
echo To start the system:
echo.
echo 1. Backend API:
echo    cd backend\IdeLogsApi
echo    dotnet run
echo.
echo 2. Frontend Dashboard (in new terminal):
echo    cd frontend
echo    npm install
echo    npm run dev
echo.
echo 3. Open browser to: http://localhost:5173
echo.
echo ======================================================================
pause
