@echo off

echo Setting up Photo Browser Application locally...

REM Start PostgreSQL database in Docker
echo Starting PostgreSQL database...
docker compose -f docker-compose.db-only.yml up -d

REM Wait for database to be ready
echo Waiting for database to be ready...
timeout /t 10 /nobreak >nul

REM Wait for database to accept connections
echo Checking database connection...
for /l %%i in (1,1,30) do (
    docker compose -f docker-compose.db-only.yml exec db pg_isready -U photo_user -d photo_browser >nul 2>&1
    if not errorlevel 1 (
        echo Database is ready!
        goto :database_ready
    )
    echo Waiting for database... (%%i/30)
    timeout /t 2 /nobreak >nul
)
:database_ready

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo Installing Python requirements...
pip install -r backend\requirements.txt

echo.
echo Starting Photo Browser Application...
echo Application will be available at: http://localhost:8000
echo.
echo Press Ctrl+C to stop the application
echo To stop the database: docker compose -f docker-compose.db-only.yml down
echo.

REM Set environment variable for local database connection
set DATABASE_URL=postgresql://photo_user:photo_pass@localhost:5432/photo_browser

REM Start the application
cd backend
python main.py

pause