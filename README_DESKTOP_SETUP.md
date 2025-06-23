# مصراوي سات - Desktop Icon Setup

This guide will help you create a desktop icon for your مصراوي سات application so you can run it by simply double-clicking the icon.

## Quick Setup (Recommended)

1. **Run the setup script:**
   ```bash
   python3 setup_desktop_icon.py
   ```

2. **That's it!** The script will:
   - Check for required dependencies
   - Create an application icon
   - Create a desktop shortcut
   - Show you the results

## Manual Setup (Alternative)

If the automatic setup doesn't work, you can do it manually:

### Step 1: Create the Icon
```bash
python3 create_icon.py
```

### Step 2: Create the Desktop Shortcut
```bash
create_desktop_shortcut.bat
```

## Files Created

After running the setup, you'll have:

- `app_icon.ico` - Application icon file
- `app_icon.png` - Icon preview image
- `launcher.py` - Application launcher with error handling
- Desktop shortcut: `مصراوي سات.lnk` (on your desktop)

## How It Works

1. **Launcher Script (`launcher.py`):**
   - Checks for required dependencies (PIL, tkinter, sqlite3)
   - Automatically installs missing dependencies if needed
   - Launches the main application with proper error handling
   - Runs without showing a console window

2. **Desktop Shortcut:**
   - Points to `pythonw.exe` (Python without console)
   - Runs the launcher script
   - Uses the custom application icon
   - Sets the working directory to your app folder

## Troubleshooting

### If the shortcut doesn't work:

1. **Check Python installation:**
   ```bash
   python3 --version
   ```

2. **Install required dependencies:**
   ```bash
   pip install Pillow
   ```

3. **Run as Administrator:**
   - Right-click on `setup_desktop_icon.py`
   - Select "Run as administrator"

4. **Manual shortcut creation:**
   - Right-click on desktop
   - Select "New" → "Shortcut"
   - Enter: `pythonw.exe "C:\path\to\your\App\launcher.py"`
   - Set working directory to your app folder
   - Set icon to `app_icon.ico`

### If you get permission errors:

- Make sure you're running the setup script as Administrator
- Check that your antivirus isn't blocking the script
- Ensure you have write permissions to your desktop folder

## Application Features

Your مصراوي سات application includes:

- **Employee Management:** Add, view, and delete employees
- **Product Management:** Add, view, and delete products with images
- **Category Management:** Organize products by categories
- **Search Functionality:** Search through products
- **Image Support:** Attach images to products
- **Arabic Interface:** Full Arabic language support

## Support

If you encounter any issues:

1. Check that all files are in the same directory
2. Ensure Python 3.6+ is installed
3. Verify that the `app.py` file exists and works
4. Try running the application directly: `python3 app.py`

---

**Note:** The desktop shortcut will only work on the computer where you created it. If you move the application to another computer, you'll need to run the setup script again. 