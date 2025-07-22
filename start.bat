@echo off

echo Building and starting Photo Browser Application...

REM Build and start the containers
docker compose up --build -d

echo.
echo Waiting for services to be ready...

REM Wait for database to be healthy
echo Waiting for database...
:wait_db
docker compose ps db | find "healthy" >nul
if errorlevel 1 (
    echo Database still starting...
    timeout /t 2 /nobreak >nul
    goto :wait_db
)
echo Database is ready!

REM Wait for application to respond
echo Waiting for application...
for /l %%i in (1,1,30) do (
    curl -s http://localhost:8000/api/images/count >nul 2>&1
    if not errorlevel 1 (
        echo Application is ready!
        goto :app_ready
    )
    echo Application still starting... (%%i/30)
    timeout /t 2 /nobreak >nul
)
:app_ready

echo.
echo Photo Browser Application is ready!
echo You can access it at: http://localhost:8000
echo.
echo To view logs: docker compose logs -f
echo To stop: docker compose down

pause