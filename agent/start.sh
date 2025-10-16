#!/bin/bash
set -e

echo "Starting application services..."

# Set default ports
export API_PORT=${API_PORT:-8081}
export UI_PORT=${PORT:-8080}

# Start the API server in the background
echo "Starting API server on port $API_PORT..."
cd /app/agent
API_PORT=$API_PORT uv run python api_server/server.py &
API_PID=$!

# Wait for API to be ready
echo "Waiting for API server to be ready..."
sleep 5

# Start the Next.js UI server
echo "Starting UI server on port $UI_PORT..."
cd /app/ui
PORT=$UI_PORT API_PORT=$API_PORT npm start &
UI_PID=$!

# Function to handle shutdown
shutdown() {
    echo "Shutting down services..."
    kill $API_PID $UI_PID 2>/dev/null
    exit 0
}

# Trap signals
trap shutdown SIGTERM SIGINT

# Wait for both processes
wait $API_PID $UI_PID
