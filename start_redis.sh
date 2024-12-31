#!/bin/bash

# Use environment variables with defaults
REDIS_PORT=${REDIS_PORT:-6379}

# Check if container exists but is not running
if docker ps -a | grep -q redis && ! docker ps | grep -q redis; then
    echo "Starting existing Redis container..."
    docker start redis
elif ! docker ps | grep -q redis; then
    echo "Creating and starting new Redis container..."
    docker run -d \
        --name redis \
        -p ${REDIS_PORT}:6379 \
        redis:latest
fi

# Wait for Redis to be fully running
until docker exec redis redis-cli -p ${REDIS_PORT} ping | grep -q PONG; do
    sleep 1
done

echo "Redis is running on port ${REDIS_PORT} with no password."
