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

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing Python requirements..."
pip install -r backend/requirements.txt

echo ""
echo "Starting Photo Browser Application..."
echo "Application will be available at: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the application"
echo "To stop the database: docker compose -f docker-compose.db-only.yml down"
echo ""

# Set environment variable for local database connection
export DATABASE_URL="postgresql://photo_user:photo_pass@localhost:5432/photo_browser"

# Start the application
cd backend
python main.py