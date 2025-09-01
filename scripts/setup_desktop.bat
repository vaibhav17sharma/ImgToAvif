@echo off
cd ..
echo AVIF Converter - Desktop Setup
echo ==============================
echo.
echo Creating desktop shortcut...

py scripts/setup_desktop.py
if %errorlevel% neq 0 (
    python scripts/setup_desktop.py
    if %errorlevel% neq 0 (
        python3 scripts/setup_desktop.py
    )
)
cd scripts

echo.
pause