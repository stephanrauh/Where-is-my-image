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
