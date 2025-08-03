#!/bin/bash

echo "Starting Authentication Service Test..."

# Check if the service is running
echo "Checking if service is running on port 8000..."
if curl -s http://localhost:8000/docs > /dev/null; then
    echo "Service is already running!"
else
    echo "Starting the service..."
    python main.py &
    SERVICE_PID=$!
    
    # Wait for service to start
    echo "Waiting for service to start..."
    sleep 5
    
    # Check if service started successfully
    if curl -s http://localhost:8000/docs > /dev/null; then
        echo "Service started successfully!"
    else
        echo "Failed to start service"
        exit 1
    fi
fi

# Run the manual test
echo "Running authentication tests..."
python manual_test.py

# If we started the service, stop it
if [ ! -z "$SERVICE_PID" ]; then
    echo "Stopping service..."
    kill $SERVICE_PID
fi

echo "Test complete!" 