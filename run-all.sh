#!/bin/bash
# Complete startup script - runs BOTH backend and frontend servers

cd "$(dirname "$0")" || exit

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Starting ACT#1-LAIT (Backend + Frontend)${NC}"
echo -e "${GREEN}========================================${NC}"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Kill any existing processes on ports 5002 and 8888
echo "Cleaning up old processes..."
pkill -f "python.*app.py" 2>/dev/null
pkill -f "python.*server.py" 2>/dev/null
sleep 1

# Start backend API (port 5002)
echo -e "${YELLOW}Starting Backend API...${NC}"
python backend_python/app.py &
BACKEND_PID=$!
echo -e "${GREEN}✓ Backend API started (PID: $BACKEND_PID)${NC}"
echo -e "${GREEN}  → http://localhost:5002/api${NC}"

# Wait for backend to start
sleep 2

# Start frontend server (port 8888)
echo -e "${YELLOW}Starting Frontend Server...${NC}"
python server.py &
FRONTEND_PID=$!
echo -e "${GREEN}✓ Frontend server started (PID: $FRONTEND_PID)${NC}"
echo -e "${GREEN}  → http://localhost:8888${NC}"

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✓ Both servers are running!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "📱 Open in browser: ${YELLOW}http://localhost:8888${NC}"
echo -e "🔐 Login with: ${YELLOW}admin@company.com / admin123${NC}"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop all servers${NC}"
echo ""

# Wait for both processes
wait

# Cleanup on exit
echo "Stopping servers..."
kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
echo -e "${GREEN}✓ All servers stopped${NC}"
