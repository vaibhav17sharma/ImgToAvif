@echo off
echo AVIF Converter - Desktop Setup
echo ==============================
echo.
echo Creating desktop shortcut...

py setup_desktop.py
if %errorlevel% neq 0 (
    python setup_desktop.py
    if %errorlevel% neq 0 (
        python3 setup_desktop.py
    )
)

echo.
pause