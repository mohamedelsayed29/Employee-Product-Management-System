#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Application Launcher for مصراوي سات
This script launches the main application with proper error handling
"""

import sys
import os
import subprocess
import tkinter as tk
from tkinter import messagebox

def check_dependencies():
    """Check if required dependencies are installed"""
    missing_deps = []
    
    try:
        import tkinter
    except ImportError:
        missing_deps.append("tkinter")
    
    try:
        import PIL
    except ImportError:
        missing_deps.append("Pillow (PIL)")
    
    try:
        import sqlite3
    except ImportError:
        missing_deps.append("sqlite3")
    
    return missing_deps

def install_dependencies():
    """Install missing dependencies"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    """Main launcher function"""
    # Change to the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Check dependencies
    missing_deps = check_dependencies()
    
    if missing_deps:
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        
        deps_text = ", ".join(missing_deps)
        result = messagebox.askyesno(
            "Missing Dependencies", 
            f"The following dependencies are missing: {deps_text}\n\nWould you like to install them automatically?"
        )
        
        if result:
            if install_dependencies():
                messagebox.showinfo("Success", "Dependencies installed successfully!\nThe application will now start.")
            else:
                messagebox.showerror("Error", "Failed to install dependencies.\nPlease install them manually:\npip install Pillow")
                return
        else:
            messagebox.showwarning("Warning", "The application may not work properly without the required dependencies.")
    
    # Launch the main application
    try:
        # Import and run the main application
        from app import init_db
        
        # Initialize database
        init_db()
        
        # Import the main application window
        import app
        
        print("Application started successfully!")
        
    except Exception as e:
        # Show error dialog
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Application Error", f"Failed to start the application:\n{str(e)}")
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 