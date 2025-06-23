#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup Desktop Icon for مصراوي سات Application
This script creates the application icon and desktop shortcut
"""

import os
import sys
import subprocess
import winreg
from PIL import Image, ImageDraw, ImageFont

def get_desktop_path():
    """Get the desktop path from Windows registry"""
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                           r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders") as key:
            desktop_path = winreg.QueryValueEx(key, "Desktop")[0]
        return desktop_path
    except:
        # Fallback to user's desktop folder
        return os.path.join(os.path.expanduser("~"), "Desktop")

def create_icon():
    """Create application icon"""
    print("Creating application icon...")
    
    # Create a 256x256 image with a blue background
    size = 256
    img = Image.new('RGBA', (size, size), (25, 118, 210, 255))  # Blue background
    draw = ImageDraw.Draw(img)
    
    # Add a white circle in the center
    circle_center = size // 2
    circle_radius = size // 3
    draw.ellipse(
        [circle_center - circle_radius, circle_center - circle_radius,
         circle_center + circle_radius, circle_center + circle_radius],
        fill=(255, 255, 255, 255)
    )
    
    # Add text "م س" (abbreviation for مصراوي سات)
    try:
        # Try to use a system font that supports Arabic
        font = ImageFont.truetype("arial.ttf", 80)
    except:
        try:
            font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 80)
        except:
            font = ImageFont.load_default()
    
    text = "م س"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    text_x = circle_center - text_width // 2
    text_y = circle_center - text_height // 2
    
    # Draw text in blue
    draw.text((text_x, text_y), text, fill=(25, 118, 210, 255), font=font)
    
    # Save as ICO file
    img.save('app_icon.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
    
    print("✓ Icon created: app_icon.ico")

def create_shortcut():
    """Create desktop shortcut using PowerShell"""
    print("Creating desktop shortcut...")
    
    # Get current directory and desktop path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    desktop_path = get_desktop_path()
    
    # Create a temporary PowerShell script file
    ps_script = f'''
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("{desktop_path}\\مصراوي سات.lnk")
$Shortcut.TargetPath = "pythonw.exe"
$Shortcut.Arguments = "{current_dir}\\launcher.py"
$Shortcut.WorkingDirectory = "{current_dir}"
$Shortcut.Description = "مصراوي سات - Employee and Product Management System"
$Shortcut.IconLocation = "{current_dir}\\app_icon.ico"
$Shortcut.Save()
'''
    
    # Write PowerShell script to temporary file
    ps_file = "create_shortcut.ps1"
    with open(ps_file, 'w', encoding='utf-8') as f:
        f.write(ps_script)
    
    try:
        # Run PowerShell script
        result = subprocess.run(['powershell', '-ExecutionPolicy', 'Bypass', '-File', ps_file], 
                              capture_output=True, text=True, check=True)
        print("✓ Desktop shortcut created successfully!")
        
        # Clean up temporary file
        if os.path.exists(ps_file):
            os.remove(ps_file)
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error creating shortcut: {e}")
        print(f"PowerShell output: {e.stdout}")
        print(f"PowerShell error: {e.stderr}")
        
        # Clean up temporary file
        if os.path.exists(ps_file):
            os.remove(ps_file)
        
        return False

def check_dependencies():
    """Check if required dependencies are available"""
    print("Checking dependencies...")
    
    # Check if PIL is available
    try:
        from PIL import Image, ImageDraw, ImageFont
        print("✓ PIL (Pillow) is available")
    except ImportError:
        print("✗ PIL (Pillow) is not available")
        print("Installing Pillow...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
            print("✓ Pillow installed successfully")
        except subprocess.CalledProcessError:
            print("✗ Failed to install Pillow")
            return False
    
    # Check if main app file exists
    if not os.path.exists("app.py"):
        print("✗ app.py not found in current directory")
        return False
    
    print("✓ All dependencies are available")
    return True

def main():
    """Main setup function"""
    print("=" * 50)
    print("مصراوي سات - Desktop Icon Setup")
    print("=" * 50)
    print()
    
    # Check dependencies
    if not check_dependencies():
        print("\nSetup failed. Please check the errors above.")
        input("Press Enter to exit...")
        return
    
    # Create icon
    create_icon()
    
    # Create shortcut
    if create_shortcut():
        print("\n" + "=" * 50)
        print("✓ Setup completed successfully!")
        print("✓ Desktop shortcut created: مصراوي سات")
        print("✓ You can now double-click the desktop icon to run the application")
        print("=" * 50)
    else:
        print("\n" + "=" * 50)
        print("✗ Setup failed!")
        print("Please try running this script as Administrator")
        print("=" * 50)
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main() 