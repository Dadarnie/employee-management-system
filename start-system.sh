#!/bin/bash
# ======================================
# ACT#1-LAIT System Startup Script
# ======================================

cd "$(dirname "$0")" || exit

echo "========================================="
echo "Starting ACT#1-LAIT System"
echo "========================================="
echo ""

# Activate virtual environment
source .venv/bin/activate 2>/dev/null || {
    echo "Creating virtual environment..."
    python3 -m venv .venv
    source .venv/bin/activate
    echo "Installing dependencies..."
    pip install -q flask flask-cors PyJWT werkzeug
}

# Kill any existing processes
pkill -9 -f "backend_python/app.py" 2>/dev/null
pkill -9 -f "server.py" 2>/dev/null
sleep 1

# Start backend API
echo "Starting Backend API (port 5002)..."
python backend_python/app.py > /tmp/backend.log 2>&1 &
sleep 2

# Start frontend server
echo "Starting Frontend Server (port 8888)..."
python server.py > /tmp/frontend.log 2>&1 &
sleep 2

echo ""
echo "========================================="
echo "✓ System is ready!"
echo "========================================="
echo ""
echo "📱 Open in browser: http://localhost:8888"
echo ""
echo "🔐 Login credentials:"
echo "   Email: admin@company.com"
echo "   Password: admin123"
echo ""
echo "🛑 To stop: Press Ctrl+C or run:"
echo "   pkill -f 'backend_python/app.py'"
echo "   pkill -f 'server.py'"
echo ""
