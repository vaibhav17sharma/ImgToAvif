# AVIF Converter

A modern web-based image converter that converts PNG, JPG, and JPEG files to AVIF format with lossless compression.

## Quick Start

### Docker (Recommended)
**Windows:** Double-click `scripts/docker_run.bat`  
**Mac/Linux:** Double-click `scripts/docker_run.sh`  
**Manual:** `docker-compose up --build`

Access at http://localhost:8080

### One-Time Desktop Setup
**Windows:** Double-click `scripts/setup_desktop.bat`  
**Mac/Linux:** Double-click `scripts/setup_desktop.sh`

### Direct Run (Python)
**Windows:** Double-click `scripts/run.bat`  
**Mac/Linux:** Double-click `scripts/run.sh`  
**Manual:** `python converter.py`

## Project Structure

```
ImgToAvif/
├── app.py              # Flask web application
├── converter.py        # Main entry point
├── requirements.txt    # Python dependencies
├── scripts/           # Setup and run scripts
│   ├── run.bat        # Windows launcher
│   ├── run.sh         # Mac/Linux launcher
│   ├── setup_desktop.bat
│   ├── setup_desktop.sh
│   └── setup_desktop.py
├── static/            # Web assets
│   ├── style.css      # Application styles
│   └── script.js      # Client-side functionality
├── templates/         # HTML templates
│   └── index.html     # Main interface
├── utils/             # Utility scripts
│   └── convert.py     # Simple CLI converter
├── Dockerfile         # Docker container setup
├── docker-compose.yml # Docker Compose configuration
└── converted/         # Output directory (auto-created)
```

## Features

- Convert PNG, JPG, JPEG to AVIF (lossless)
- Batch conversion (up to 50 files, 100MB total)
- Image previews for input and output files
- Real-time file size comparison and savings
- Auto-cleanup timer (10 minutes)
- Drag & drop interface
- Cross-platform support (Windows/Mac/Linux)
- Single Page Application (SPA) experience
- Automatic browser opening
- Auto-detects Python installation

## System Requirements

### Docker (Recommended)
- Docker and Docker Compose
- No Python installation needed

### Python Method
- Python 3.7+ (auto-detected, installation guidance provided)
- Internet connection (for initial dependency installation)

## Sharing

To share with others, provide the entire project folder.

**Recipients:** 
- **Docker:** Double-click `scripts/docker_run.bat` (Windows) or `scripts/docker_run.sh` (Mac/Linux)
- **Python:** Double-click `scripts/setup_desktop.bat` (Windows) or `scripts/setup_desktop.sh` (Mac/Linux) for one-time setup

## How It Works

1. **Auto-detects Python** - Tries `python`, `python3`, and `py` commands
2. **Installs dependencies** - Automatically installs Flask, Pillow, and pillow-avif-plugin
3. **Starts web server** - Runs on localhost:8080
4. **Opens browser** - Automatically opens the converter interface

## Development

- **Flask Backend:** `app.py` - Handles file upload, conversion, and API
- **Frontend:** `static/` - Modern CSS and JavaScript
- **Templates:** `templates/` - Jinja2 HTML templates
- **Entry Point:** `converter.py` - Auto-setup and server launcher

## Troubleshooting

If you get permission errors:
- **Windows**: Run Command Prompt as Administrator
- **Mac/Linux**: Use `sudo python converter.py` if needed

If dependencies fail to install:
```bash
pip install Flask Pillow pillow-avif-plugin
python converter.py
```