#!/bin/bash

# Use environment variables with defaults
RABBITMQ_USER=${RABBITMQ_USER:-guest}
RABBITMQ_PASS=${RABBITMQ_PASS:-guest}
RABBITMQ_PORT=${RABBITMQ_PORT:-5672}
RABBITMQ_MANAGEMENT_PORT=${RABBITMQ_MANAGEMENT_PORT:-15672}

# Check if container exists but is not running
if docker ps -a | grep -q rabbitmq && ! docker ps | grep -q rabbitmq; then
    echo "Starting existing RabbitMQ container..."
    docker start rabbitmq
elif ! docker ps | grep -q rabbitmq; then
    echo "Creating and starting new RabbitMQ container..."
    docker run -d \
        --name rabbitmq \
        --hostname rabbitmq \
        -p ${RABBITMQ_PORT}:5672 \
        -p ${RABBITMQ_MANAGEMENT_PORT}:15672 \
        -e RABBITMQ_USER=${RABBITMQ_USER} \
        -e RABBITMQ_PASS=${RABBITMQ_PASS} \
        rabbitmq:management
fi

# Wait for RabbitMQ to be fully running
until curl -s -f http://localhost:${RABBITMQ_MANAGEMENT_PORT} >/dev/null 2>&1; do
    sleep 1
done

echo "RabbitMQ is running (credentials: ${RABBITMQ_USER}/${RABBITMQ_PASS}). Management console available at http://localhost:${RABBITMQ_MANAGEMENT_PORT}"
