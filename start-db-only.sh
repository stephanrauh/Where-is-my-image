#!/bin/bash

echo "Setting up Photo Browser Application locally..."

# Start PostgreSQL database in Docker
echo "Starting PostgreSQL database..."
docker compose -f docker-compose.db-only.yml up -d

# Wait for database to be ready
echo "Waiting for database to be ready..."
sleep 10

# Wait for database to accept connections
echo "Checking database connection..."
for i in {1..30}; do
    if docker compose -f docker-compose.db-only.yml exec db pg_isready -U photo_user -d photo_browser > /dev/null 2>&1; then
        echo "Database is ready!"
        break
    fi
    echo "Waiting for database... ($i/30)"
    sleep 2
done

