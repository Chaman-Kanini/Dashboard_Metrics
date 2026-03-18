@echo off
echo ======================================================================
echo Starting IDE Logs Dashboard - All Services
echo ======================================================================
echo.

echo Starting Backend API...
start "Backend API" cmd /k "cd backend\IdeLogsApi && dotnet run"

timeout /t 5 /nobreak >nul

echo Starting Frontend Dashboard...
start "Frontend Dashboard" cmd /k "cd frontend && npm run dev"

echo.
echo ======================================================================
echo Services Starting...
echo ======================================================================
echo.
echo Backend API: http://localhost:5000
echo Swagger UI: http://localhost:5000/swagger
echo Frontend Dashboard: http://localhost:5173
echo.
echo Press any key to stop all services...
pause >nul

echo.
echo Stopping services...
taskkill /FI "WINDOWTITLE eq Backend API*" /T /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Frontend Dashboard*" /T /F >nul 2>&1

echo Services stopped.
