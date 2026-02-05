#!/bin/bash
# Employee Management System - Setup & Start Script

echo "🚀 Starting Employee Management System..."
echo ""

# Kill any existing processes on port 5002
pkill -f "python.*app.py" 2>/dev/null || true
sleep 1

# Change to project directory
cd "$(dirname "$0")" || exit

# Start backend server
echo "Starting backend server on port 5002..."
python backend_python/app.py &
BACKEND_PID=$!

sleep 2

# Check if backend started
if curl -s http://localhost:5002/health > /dev/null 2>&1; then
    echo "✅ Backend server running on http://localhost:5002"
    echo ""
    echo "🌐 Frontend: http://localhost:8888"
    echo ""
    echo "📝 Login Credentials:"
    echo "  Email: admin@company.com"
    echo "  Password: admin123"
    echo ""
    echo "⏹️  Press Ctrl+C to stop the server"
    echo ""
    
    # Keep the script running
    wait $BACKEND_PID
else
    echo "❌ Backend failed to start"
    exit 1
fi
