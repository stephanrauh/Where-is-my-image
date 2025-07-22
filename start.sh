#!/bin/bash

echo "Building and starting Photo Browser Application..."

# Build and start the containers
docker compose up --build -d

echo ""
echo "Waiting for services to be ready..."

# Wait for database to be healthy
echo "Waiting for database..."
while ! docker compose ps db | grep -q "healthy"; do
    sleep 2
    echo "Database still starting..."
done
echo "Database is ready!"

# Wait for application to respond
echo "Waiting for application..."
for i in {1..30}; do
    if curl -s http://localhost:8000/api/images/count > /dev/null 2>&1; then
        echo "Application is ready!"
        break
    fi
    echo "Application still starting... ($i/30)"
    sleep 2
done

echo ""
echo "Photo Browser Application is ready!"
echo "You can access it at: http://localhost:8000"
echo ""
echo "To view logs: docker compose logs -f"
echo "To stop: docker compose down"