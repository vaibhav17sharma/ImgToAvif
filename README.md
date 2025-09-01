# PNG/JPG to AVIF Converter

A portable web-based image converter that converts PNG, JPG, and JPEG files to AVIF format with lossless compression.

## Quick Start

### Windows
Double-click `run.bat`

### Mac/Linux
Double-click `run.sh` or run in terminal:
```bash
./run.sh
```

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
- `run.bat` (Windows)
- `run.sh` (Mac/Linux)  
- `converter.py`
- `app.py`
- `templates/index.html`

**Recipients:** Just double-click the appropriate run file for your system!

## Troubleshooting

If you get permission errors:
- **Windows**: Run Command Prompt as Administrator
- **Mac/Linux**: Use `sudo python converter.py` if needed

If dependencies fail to install:
```bash
pip install Flask Pillow pillow-avif-plugin
python converter.py
```