#!/usr/bin/env python3
import subprocess
import sys
import os
import webbrowser
import threading
import time
import platform

def setup_venv_and_install():
    """Create venv and install packages (Mac/Linux)"""
    import venv
    
    venv_path = 'venv'
    if not os.path.exists(venv_path):
        print("Creating virtual environment...")
        venv.create(venv_path, with_pip=True)
    
    # Get venv python and pip paths
    if platform.system() == 'Windows':
        python_exe = os.path.join(venv_path, 'Scripts', 'python')
        pip_exe = os.path.join(venv_path, 'Scripts', 'pip')
    else:
        python_exe = os.path.join(venv_path, 'bin', 'python')
        pip_exe = os.path.join(venv_path, 'bin', 'pip')
    
    requirements = ['Flask', 'Pillow', 'pillow-avif-plugin', 'pillow-heif']
    
    print("Installing dependencies in virtual environment...")
    for req in requirements:
        print(f"Installing {req}...")
        try:
            subprocess.check_call([pip_exe, 'install', req])
        except subprocess.CalledProcessError:
            print(f"Failed to install {req}")
            return None
    
    return python_exe

def install_requirements():
    """Install required packages (Windows fallback)"""
    requirements = ['Flask', 'Pillow', 'pillow-avif-plugin', 'pillow-heif']
    
    print("Installing dependencies...")
    for req in requirements:
        print(f"Installing {req}...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', req])
        except subprocess.CalledProcessError:
            print(f"Failed to install {req}")
            return False
    return True

def cleanup_old_files():
    """Remove files older than 1 hour from converted folder"""
    current_time = time.time()
    if os.path.exists('converted'):
        for filename in os.listdir('converted'):
            filepath = os.path.join('converted', filename)
            if os.path.isfile(filepath) and current_time - os.path.getctime(filepath) > 3600:
                try:
                    os.remove(filepath)
                except:
                    pass

def cleanup_files():
    """Background cleanup task"""
    while True:
        time.sleep(3600)  # Wait 1 hour
        cleanup_old_files()

def main():
    print("Image Converter - AVIF & HEIC to PNG")
    print("=" * 30)
    print(f"Running on {platform.system()} {platform.release()}")
    print()
    
    # Check if packages are installed
    try:
        import flask
        import PIL
        import pillow_avif
        import pillow_heif
    except ImportError:
        print("Installing required packages...")
        
        # Use venv on Mac/Linux, direct install on Windows
        if platform.system() in ['Darwin', 'Linux']:
            python_exe = setup_venv_and_install()
            if not python_exe:
                print("Failed to setup environment. Please run manually:")
                print("python3 -m venv venv")
                print("source venv/bin/activate")
                print("pip install Flask Pillow pillow-avif-plugin pillow-heif")
                input("Press Enter to exit...")
                return
            
            # Restart with venv python
            print("Restarting with virtual environment...")
            subprocess.call([python_exe, os.path.abspath(__file__)])
            return
        else:
            # Windows - direct install
            if not install_requirements():
                print("Failed to install packages. Please run manually:")
                print("pip install Flask Pillow pillow-avif-plugin pillow-heif")
                input("Press Enter to exit...")
                return
    
    # Create required directories
    os.makedirs('converted', exist_ok=True)
    
    # Clean old files on startup
    cleanup_old_files()
    
    # Start cleanup thread
    cleanup_thread = threading.Thread(target=cleanup_files, daemon=True)
    cleanup_thread.start()
    
    # Import and run Flask app
    try:
        from app import app
        print("Starting converter...")
        print("Opening browser...")
        
        # Open browser after short delay
        def open_browser():
            time.sleep(1.5)
            webbrowser.open('http://localhost:8080')
        
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.start()
        
        app.run(host='127.0.0.1', port=8080, debug=False)
        
    except ImportError:
        print("Error: app.py not found in current directory")
    except Exception as e:
        print(f"Error starting application: {e}")

if __name__ == '__main__':
    main()