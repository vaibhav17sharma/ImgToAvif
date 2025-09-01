# PNG/JPG to AVIF Converter

A portable web-based image converter that converts PNG, JPG, and JPEG files to AVIF format with lossless compression.

## Quick Start

### One-Time Desktop Setup (Recommended)
**Windows:** Double-click `setup_desktop.bat`  
**Mac/Linux:** Double-click `setup_desktop.sh`

This creates a desktop icon you can click anytime!

### Direct Run (Alternative)
**Windows:** Double-click `run.bat`  
**Mac/Linux:** Double-click `run.sh`

### Manual (if you have Python)
```bash
python converter.py
```

## Features

- Convert PNG, JPG, JPEG to AVIF (lossless)
- Batch conversion (up to 50 files, 100MB total)
- Automatic browser opening
- Auto-cleanup of converted files after 1 hour
- Cross-platform support (Windows/Mac/Linux)
- No manual setup required

## System Requirements

- Python 3.7+ (auto-detected, installation guidance provided)
- Internet connection (for initial dependency installation)

## How It Works

1. **Auto-detects Python** - Tries `python`, `python3`, and `py` commands
2. **Installs dependencies** - Automatically installs Flask, Pillow, and pillow-avif-plugin
3. **Starts web server** - Runs on localhost:8080
4. **Opens browser** - Automatically opens the converter interface

## Sharing

To share with others, provide these files:
- `setup_desktop.bat` (Windows setup)
- `setup_desktop.sh` (Mac/Linux setup)
- `setup_desktop.py` (Desktop installer)
- `run.bat` (Windows)
- `run.sh` (Mac/Linux)  
- `converter.py`
- `app.py`
- `templates/index.html`

**Recipients:** Double-click `setup_desktop.bat` (Windows) or `setup_desktop.sh` (Mac/Linux) for one-time setup, then use the desktop icon!

## Troubleshooting

If you get permission errors:
- **Windows**: Run Command Prompt as Administrator
- **Mac/Linux**: Use `sudo python converter.py` if needed

If dependencies fail to install:
```bash
pip install Flask Pillow pillow-avif-plugin
python converter.py
```