#!/bin/bash
# Debug script to test the full system

echo "========================================="
echo "System Test Script"
echo "========================================="
echo ""

# Test 1: Check if backend is running
echo "1️⃣  Testing backend connection..."
if curl -s http://localhost:5002/api/auth/login -H "Content-Type: application/json" -d '{}' 2>/dev/null | grep -q "error\|missing"; then
    echo "   ✓ Backend is responsive"
else
    echo "   ✗ Backend not responding properly"
    exit 1
fi

# Test 2: Login and get token
echo ""
echo "2️⃣  Testing login..."
TOKEN=$(curl -s -X POST http://localhost:5002/api/auth/login \
    -H "Content-Type: application/json" \
    -d '{"email":"admin@company.com","password":"admin123"}' | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('token', ''))" 2>/dev/null)

if [ -z "$TOKEN" ]; then
    echo "   ✗ Failed to get token"
    exit 1
fi
echo "   ✓ Login successful"
echo "   Token: ${TOKEN:0:20}..."

# Test 3: Get employees
echo ""
echo "3️⃣  Testing employees endpoint..."
RESPONSE=$(curl -s http://localhost:5002/api/employees \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json")

COUNT=$(echo "$RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(len(data) if isinstance(data, list) else 0)" 2>/dev/null)

if [ "$COUNT" -gt 0 ]; then
    echo "   ✓ Found $COUNT employees"
    echo "$RESPONSE" | python3 -m json.tool 2>/dev/null | head -30
else
    echo "   ✗ No employees found or error occurred"
    echo "   Response: $RESPONSE"
fi

# Test 4: Get password logs
echo ""
echo "4️⃣  Testing password logs endpoint..."
LOGS_RESPONSE=$(curl -s http://localhost:5002/api/password-logs \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json")

echo "   Response: $LOGS_RESPONSE" | python3 -m json.tool 2>/dev/null | head -20

# Test 5: Get login logs
echo ""
echo "5️⃣  Testing login logs endpoint..."
LOGIN_RESPONSE=$(curl -s http://localhost:5002/api/login-logs \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json")

echo "   Response: $LOGIN_RESPONSE" | python3 -m json.tool 2>/dev/null | head -20

# Test 6: Get deleted employees
echo ""
echo "6️⃣  Testing deleted employees endpoint..."
DELETED_RESPONSE=$(curl -s http://localhost:5002/api/deleted-employees \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json")

echo "   Response: $DELETED_RESPONSE" | python3 -m json.tool 2>/dev/null | head -20

echo ""
echo "========================================="
echo "✓ Test complete!"
echo "========================================="
