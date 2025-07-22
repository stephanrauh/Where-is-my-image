#!/bin/bash

echo "Stopping Photo Browser Application database..."
docker compose -f docker-compose.db-only.yml down

echo "Database stopped."