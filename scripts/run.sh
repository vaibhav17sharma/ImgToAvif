#!/bin/bash
cd ..
echo "PNG/JPG to AVIF Converter"
echo "=============================="

# Check for Python
if command -v python3 &> /dev/null; then
    echo "Found Python3, starting converter..."
    python3 converter.py
elif command -v python &> /dev/null; then
    echo "Found Python, starting converter..."
    python converter.py
else
    echo "ERROR: Python not found!"
    echo ""
    
    # OS-specific installation instructions
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "On macOS, install Python via:"
        echo "1. Homebrew: brew install python3"
        echo "2. Official installer: https://www.python.org/downloads/"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "On Linux, install Python via:"
        echo "Ubuntu/Debian: sudo apt install python3 python3-pip"
        echo "CentOS/RHEL: sudo yum install python3 python3-pip"
        echo "Arch: sudo pacman -S python python-pip"
    fi
    
    echo ""
    echo "Press Enter to exit..."
    read
fi