# Employee & Product Management System

A desktop application for managing employees and products, with full Arabic language support. The app allows you to add, view, and delete employees and products, organize products by categories, search, and attach images to products.

## Features
- **Employee Management:** Add, view, and delete employees
- **Product Management:** Add, view, and delete products with images
- **Category Management:** Organize products by categories
- **Search Functionality:** Search through products
- **Image Support:** Attach images to products
- **Arabic Interface:** Full Arabic language support

## Requirements
- Python 3.6+
- [Pillow](https://pypi.org/project/Pillow/) (for image support)
- tkinter (usually included with Python)
- sqlite3 (included with Python)

## Quick Start
1. **Install dependencies:**
   ```bash
   pip install Pillow
   ```
2. **Run the application:**
   ```bash
   python app.py
   ```

## Desktop Shortcut Setup (Windows)
To create a desktop shortcut for easy launching:

1. **Automatic Setup (Recommended):**
   ```bash
   python setup_desktop_icon.py
   ```
   This will:
   - Check for required dependencies
   - Create an application icon
   - Create a desktop shortcut

2. **Manual Setup:**
   - Run `python create_icon.py` to generate the icon
   - Run `create_desktop_shortcut.bat` to create the shortcut

## How It Works
- The launcher script (`launcher.py`) checks for dependencies and launches the main app with error handling.
- The desktop shortcut uses `pythonw.exe` to run the app without a console window, using the custom icon.

## Troubleshooting
- Ensure Python 3.6+ is installed
- Install dependencies with `pip install Pillow`
- If you get permission errors, run setup scripts as Administrator
- If the shortcut doesn't work, try creating it manually as described above

## Support
- Make sure all files are in the same directory
- If you move the app to another computer, re-run the setup script
- For issues, try running `python app.py` directly

---
