#!/bin/bash
set -e

# Health+ Agent - Docker Startup Script
# This script starts both the backend API server and frontend application

echo "=========================================="
echo "Health+ Agent - Starting Services"
echo "=========================================="
echo ""

# Load environment variables from .env if it exists
if [ -f /agent/.env ]; then
  echo "📝 Loading environment variables from /agent/.env..."
  set -a
  source /agent/.env
  set +a
  echo "✅ Environment variables loaded"
else
  echo "⚠️  /agent/.env not found, using container environment variables"
fi

# Verify GOOGLE_API_KEY is set
if [ -z "$GOOGLE_API_KEY" ]; then
  echo "❌ ERROR: GOOGLE_API_KEY is not set!"
  echo "   Please set GOOGLE_API_KEY in your .env file or as an environment variable"
  exit 1
fi

echo "✅ GOOGLE_API_KEY is set"
echo ""

# Start backend API server
echo "🚀 Starting backend API server..."
cd /agent

# Activate virtual environment and start backend
if [ -f /agent/.venv/bin/activate ]; then
  source /agent/.venv/bin/activate
  python -m uvicorn api_server.server:app --host 0.0.0.0 --port 8000 &
else
  echo "⚠️  Virtual environment not found at /agent/.venv"
  echo "   Attempting to use system python..."
  python -m uvicorn api_server.server:app --host 0.0.0.0 --port 8000 &
fi

BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"

# Wait for backend to be ready
echo "⏳ Waiting for backend to be ready..."
sleep 3

# Start frontend
echo "🚀 Starting frontend..."
cd /app/frontend
pnpm start &
FRONTEND_PID=$!
echo "   Frontend PID: $FRONTEND_PID"

echo ""
echo "=========================================="
echo "✅ Services Started Successfully!"
echo "=========================================="
echo ""
echo "Frontend:  http://localhost:3000"
echo "Backend:   http://localhost:8000"
echo "API Docs:  http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"
echo "=========================================="
echo ""

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID

