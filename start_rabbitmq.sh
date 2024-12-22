#!/bin/bash

# Check if container exists but is not running
if docker ps -a | grep -q rabbitmq && ! docker ps | grep -q rabbitmq; then
    echo "Starting existing RabbitMQ container..."
    docker start rabbitmq
elif ! docker ps | grep -q rabbitmq; then
    echo "Creating and starting new RabbitMQ container..."
    docker run -d \
        --name rabbitmq \
        --hostname rabbitmq \
        -p 5672:5672 \
        -p 15672:15672 \
        rabbitmq:management
fi

# Wait for RabbitMQ to be fully running
echo "Waiting for RabbitMQ to start..."
until curl -s -f http://localhost:15672 >/dev/null 2>&1; do
    sleep 1
done

echo "RabbitMQ is running (credentials: guest/guest). Management console available at http://localhost:15672"
