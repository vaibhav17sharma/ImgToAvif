#!/usr/bin/env python3
import os
import sys
import platform
import subprocess

def create_windows_shortcut():
    """Create Windows desktop shortcut using VBS script"""
    # Try multiple desktop locations
    desktop_paths = [
        os.path.join(os.path.expanduser("~"), "Desktop"),
        os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop"),
        os.environ.get('USERPROFILE', '') + "\\Desktop",
        os.environ.get('USERPROFILE', '') + "\\OneDrive\\Desktop"
    ]
    
    desktop = None
    for path in desktop_paths:
        if os.path.exists(path):
            desktop = path
            break
    
    if not desktop:
        raise Exception("Could not find Desktop folder")
    
    shortcut_path = os.path.join(desktop, "AVIF Converter.lnk")
    target = os.path.join(os.getcwd(), "scripts", "run.bat")
    
    print(f"Creating shortcut at: {shortcut_path}")
    print(f"Target: {target}")
    
    # Create VBS script to make shortcut
    vbs_script = f'''Set oWS = WScript.CreateObject("WScript.Shell")
Set oLink = oWS.CreateShortcut("{shortcut_path}")
oLink.TargetPath = "{target}"
oLink.WorkingDirectory = "{os.getcwd()}"
oLink.Save
'''
    
    # Write and execute VBS script
    vbs_file = "create_shortcut.vbs"
    with open(vbs_file, 'w') as f:
        f.write(vbs_script)
    
    try:
        result = subprocess.run(["cscript", "//nologo", vbs_file], capture_output=True, text=True)
        os.remove(vbs_file)
        if result.returncode == 0:
            print(f"Desktop shortcut created: {shortcut_path}")
            if os.path.exists(shortcut_path):
                print("Shortcut file confirmed to exist")
            else:
                print("Warning: Shortcut creation reported success but file not found")
        else:
            raise Exception(f"VBS script failed: {result.stderr}")
    except Exception as e:
        if os.path.exists(vbs_file):
            os.remove(vbs_file)
        raise e

def create_mac_shortcut():
    """Create macOS desktop shortcut"""
    desktop = os.path.expanduser("~/Desktop")
    app_name = "AVIF Converter.command"
    path = os.path.join(desktop, app_name)
    
    script_content = f"""#!/bin/bash
cd "{os.path.join(os.getcwd(), 'scripts')}"
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
Exec=bash -c "cd '{os.path.join(os.getcwd(), 'scripts')}' && ./run.sh"
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