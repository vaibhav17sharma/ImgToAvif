#!/usr/bin/env python3
import os
import sys
import platform
import subprocess

def create_windows_shortcut():
    """Create Windows desktop shortcut"""
    try:
        import winshell
        from win32com.client import Dispatch
    except ImportError:
        print("Installing shortcut dependencies...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'winshell', 'pywin32'])
        import winshell
        from win32com.client import Dispatch
    
    desktop = winshell.desktop()
    path = os.path.join(desktop, "AVIF Converter.lnk")
    target = os.path.join(os.getcwd(), "run.bat")
    
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = os.getcwd()
    shortcut.IconLocation = target
    shortcut.save()
    
    print(f"Desktop shortcut created: {path}")

def create_mac_shortcut():
    """Create macOS desktop shortcut"""
    desktop = os.path.expanduser("~/Desktop")
    app_name = "AVIF Converter.command"
    path = os.path.join(desktop, app_name)
    
    script_content = f"""#!/bin/bash
cd "{os.getcwd()}"
./run.sh
"""
    
    with open(path, 'w') as f:
        f.write(script_content)
    
    os.chmod(path, 0o755)
    print(f"Desktop shortcut created: {path}")

def create_linux_shortcut():
    """Create Linux desktop shortcut"""
    desktop = os.path.expanduser("~/Desktop")
    path = os.path.join(desktop, "AVIF Converter.desktop")
    
    content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=AVIF Converter
Comment=Convert images to AVIF format
Exec=bash -c "cd '{os.getcwd()}' && ./run.sh"
Icon=applications-graphics
Terminal=true
Categories=Graphics;Photography;
"""
    
    with open(path, 'w') as f:
        f.write(content)
    
    os.chmod(path, 0o755)
    print(f"Desktop shortcut created: {path}")

def main():
    print("AVIF Converter - Desktop Setup")
    print("=" * 30)
    
    system = platform.system()
    
    try:
        if system == "Windows":
            create_windows_shortcut()
        elif system == "Darwin":
            create_mac_shortcut()
        elif system == "Linux":
            create_linux_shortcut()
        else:
            print(f"Unsupported system: {system}")
            return
        
        print("\nSetup complete! You can now:")
        print("1. Find 'AVIF Converter' on your desktop")
        print("2. Double-click it to start the converter")
        print("3. Delete this folder if you want - the shortcut will still work")
        
    except Exception as e:
        print(f"Failed to create shortcut: {e}")
        print("You can still use the converter by running:")
        if system == "Windows":
            print("  run.bat")
        else:
            print("  ./run.sh")

if __name__ == '__main__':
    main()