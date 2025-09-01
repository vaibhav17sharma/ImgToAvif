#!/bin/bash
echo "Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Starting PNG to AVIF Converter Web App..."
echo "Open http://localhost:8080 in your browser"
python app.py