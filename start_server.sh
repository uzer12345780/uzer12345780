#!/bin/bash

# KoloCloud Server Startup Script for Linux/Mac
echo "🚀 Starting KoloCloud Server..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r backend/requirements.txt

# Check if .env file exists
if [ ! -f "config/.env" ]; then
    echo "⚠️  Warning: config/.env not found. Using default configuration."
    echo "📝 Please copy config/.env.example to config/.env and configure it."
fi

# Create necessary directories
mkdir -p data/users
mkdir -p data/temp
mkdir -p data/logs

# Export Flask app
export FLASK_APP=backend/app.py
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Run the server
echo "🌐 Starting server on http://localhost:5000"
echo "Press Ctrl+C to stop the server"
python3 backend/app.py
