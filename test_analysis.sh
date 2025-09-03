#!/bin/bash

echo "Testing Analysis API..."
echo "========================"

# Test 1: Check if backend is running
echo -e "\n1. Testing backend health..."
curl -s http://localhost:8000/ | jq . || echo "Backend not responding"

# Test 2: Test with valid company (XPP)
echo -e "\n2. Testing with valid company (XPP)..."
response=$(curl -s -X POST http://localhost:8000/api/analysis/start \
  -H "Content-Type: application/json" \
  -d '{"company": "XP Power", "ticker": "XPP"}')
echo "Response: $response"
task_id=$(echo $response | jq -r '.task_id')

if [ "$task_id" != "null" ]; then
  echo "Task ID: $task_id"
  sleep 3
  echo "Checking status..."
  curl -s http://localhost:8000/api/analysis/status/$task_id | jq .
else
  echo "No task_id returned - checking for error message"
  echo $response | jq .
fi

# Test 3: Test with empty company
echo -e "\n3. Testing with empty company (TEST)..."
response=$(curl -s -X POST http://localhost:8000/api/analysis/start \
  -H "Content-Type: application/json" \
  -d '{"company": "Test Company", "ticker": "TEST"}')
echo "Response: $response"
echo $response | jq .

# Test 4: Test through Vite proxy
echo -e "\n4. Testing through Vite proxy..."
response=$(curl -s -X POST http://localhost:3000/api/analysis/start \
  -H "Content-Type: application/json" \
  -d '{"company": "XP Power", "ticker": "XPP"}')
echo "Response: $response"
echo $response | jq .

echo -e "\nTest complete!"