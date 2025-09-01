# AVIF Converter

A modern web-based image converter that converts PNG, JPG, and JPEG files to AVIF format with lossless compression.

## Quick Start

### One-Time Desktop Setup (Recommended)
**Windows:** Double-click `scripts/setup_desktop.bat`  
**Mac/Linux:** Double-click `scripts/setup_desktop.sh`

This creates a desktop icon you can click anytime!

### Direct Run (Alternative)
**Windows:** Double-click `scripts/run.bat`  
**Mac/Linux:** Double-click `scripts/run.sh`

### Manual (if you have Python)
```bash
python converter.py
```

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
├── docs/              # Documentation
│   ├── README.md      # Detailed documentation
│   └── Dockerfile     # Container setup
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

## System Requirements

- Python 3.7+ (auto-detected, installation guidance provided)
- Internet connection (for initial dependency installation)

## Sharing

To share with others, provide the entire project folder.

**Recipients:** Double-click `scripts/setup_desktop.bat` (Windows) or `scripts/setup_desktop.sh` (Mac/Linux) for one-time setup, then use the desktop icon!

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