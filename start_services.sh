#!/bin/bash

# Start both Node.js and Python services concurrently

echo "Starting Liver Disease Prediction Services..."

# Function to cleanup processes on exit
cleanup() {
    echo "Shutting down services..."
    kill $(jobs -p) 2>/dev/null
    exit
}

# Set up cleanup trap
trap cleanup SIGINT SIGTERM

# Start Python ML service in background
echo "Starting Python ML service on port 8001..."
python3 start_ml_service.py &
ML_PID=$!

# Wait a moment for ML service to start
sleep 2

# Start Node.js service
echo "Starting Node.js application on port 5000..."
npm run dev &
NODE_PID=$!

# Wait for both processes
wait $ML_PID $NODE_PID