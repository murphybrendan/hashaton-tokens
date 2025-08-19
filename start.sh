#!/bin/bash

# MTG Token Creator - Startup Script
echo "🃏 Starting MTG Token Creator..."
echo "📱 Opening browser to http://localhost:5000"
echo "⏹️  Press Ctrl+C to stop the server"
echo "-" * 50

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Start the server
python3 run.py
