#!/bin/bash

echo "Building and starting Photo Browser Application..."

# Build and start the containers
docker compose up --build -d

echo ""
echo "Photo Browser Application is starting up..."
echo "Please wait a moment for the services to initialize."
echo ""
echo "Once ready, you can access the application at:"
echo "  http://localhost:8000"
echo ""
echo "To view logs: docker compose logs -f"
echo "To stop: docker compose down"