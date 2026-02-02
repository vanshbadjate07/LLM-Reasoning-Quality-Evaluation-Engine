#!/bin/bash

# ReasonEval Launcher Script
# Starts Ollama (if not running) and the ReasonEval Streamlit App

echo "========================================"
echo "🚀 Starting ReasonEval System..."
echo "========================================"

# 1. Check if Ollama is running
if ! pgrep -x "ollama" > /dev/null
then
    echo "⭕ Ollama is not running. Starting Ollama..."
    ollama serve > /dev/null 2>&1 &
    
    # Wait for Ollama to initialize
    echo "⏳ Waiting for Ollama to start (10s)..."
    sleep 10
else
    echo "✅ Ollama is already running."
fi

# 2. Check/Activate Virtual Environment (Optional, based on user setup)
if [ -d "venv" ]; then
    echo "🐍 Activating Python Virtual Environment..."
    source venv/bin/activate
fi

# 3. Start Streamlit App
echo "💻 Launching User Interface..."
echo "========================================"
echo "👉 The app will open in your browser shortly."
echo "👉 Press Ctrl+C to stop the system."
echo "========================================"

streamlit run streamlit_app.py
