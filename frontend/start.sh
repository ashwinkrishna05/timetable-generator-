#!/bin/bash

echo "🚀 Starting School Timetable Generator Frontend..."
echo "📱 Frontend: http://localhost:3000"
echo "🔗 Backend API: http://localhost:8000"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Start the development server
echo "🌐 Starting development server..."
npm run dev
