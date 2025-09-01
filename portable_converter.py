#!/usr/bin/env python3
import subprocess
import sys
import os
import webbrowser
import threading
import time
import platform

def install_requirements():
    """Install required packages"""
    requirements = ['Flask==2.3.3', 'Pillow==10.0.1', 'pillow-avif-plugin==1.4.3']
    
    for req in requirements:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', req], 
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            print(f"Failed to install {req}")
            return False
    return True

def cleanup_old_files():
    """Remove files older than 10 minutes from converted folder"""
    current_time = time.time()
    if os.path.exists('converted'):
        for filename in os.listdir('converted'):
            filepath = os.path.join('converted', filename)
            if os.path.isfile(filepath) and current_time - os.path.getctime(filepath) > 600:
                try:
                    os.remove(filepath)
                except:
                    pass

def cleanup_files():
    """Background cleanup task"""
    while True:
        time.sleep(600)  # Wait 10 minutes
        cleanup_old_files()

def main():
    print("PNG/JPG to AVIF Converter")
    print("=" * 30)
    print(f"Running on {platform.system()} {platform.release()}")
    print()
    
    # Install requirements
    print("Installing dependencies...")
    if not install_requirements():
        print("Failed to install dependencies. Please install manually:")
        print("pip install Flask Pillow pillow-avif-plugin")
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