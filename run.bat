@echo off
echo PNG/JPG to AVIF Converter
echo ==============================

REM Check for Python
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo Found Python, starting converter...
    python converter.py
    goto end
)

python3 --version >nul 2>&1
if %errorlevel% == 0 (
    echo Found Python3, starting converter...
    python3 converter.py
    goto end
)

py --version >nul 2>&1
if %errorlevel% == 0 (
    echo Found Python via py launcher, starting converter...
    py converter.py
    goto end
)

echo ERROR: Python not found!
echo Please install Python from: https://www.python.org/downloads/
echo Make sure to check "Add Python to PATH" during installation
pause

:end
pause