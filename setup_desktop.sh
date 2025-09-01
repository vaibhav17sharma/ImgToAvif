#!/bin/bash
echo "AVIF Converter - Desktop Setup"
echo "=============================="
echo ""
echo "Creating desktop shortcut..."

if command -v python3 &> /dev/null; then
    python3 setup_desktop.py
elif command -v python &> /dev/null; then
    python setup_desktop.py
else
    echo "ERROR: Python not found!"
    exit 1
fi

echo ""
echo "Press Enter to continue..."
read