#!/bin/bash
# Startup script for ACT#1-LAIT application

cd "$(dirname "$0")" || exit

# Activate virtual environment
source .venv/bin/activate

echo "Starting ACT#1-LAIT..."
echo "========================"

# Start backend API (port 5000)
python backend_python/app.py &
BACKEND_PID=$!
echo "✓ Backend API started (PID: $BACKEND_PID) on http://localhost:5000"

# Start frontend server (port 7777)
python server.py &
FRONTEND_PID=$!
echo "✓ Frontend server started (PID: $FRONTEND_PID) on http://localhost:7777"

echo "========================"
echo "Application running!"
echo "Access at: http://localhost:7777"
echo ""
echo "To stop: kill $BACKEND_PID $FRONTEND_PID"
echo ""

# Keep script running
wait
