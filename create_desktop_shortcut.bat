@echo off
echo Creating Desktop Shortcut for مصراوي سات Application...
echo.

REM Get the current directory (where the script is located)
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

REM Get the desktop path
for /f "tokens=2*" %%a in ('reg query "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders" /v Desktop 2^>nul') do set "DESKTOP=%%b"

REM Create the shortcut using PowerShell
powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP%\مصراوي سات.lnk'); $Shortcut.TargetPath = 'pythonw.exe'; $Shortcut.Arguments = '\"%SCRIPT_DIR%\launcher.py\"'; $Shortcut.WorkingDirectory = '%SCRIPT_DIR%'; $Shortcut.Description = 'مصراوي سات - Employee and Product Management System'; $Shortcut.IconLocation = '%SCRIPT_DIR%\app_icon.ico'; $Shortcut.Save()}"

if exist "%DESKTOP%\مصراوي سات.lnk" (
    echo ✓ Desktop shortcut created successfully!
    echo ✓ Location: %DESKTOP%\مصراوي سات.lnk
    echo.
    echo You can now double-click the desktop icon to run the application.
) else (
    echo ✗ Failed to create desktop shortcut.
    echo Please run this script as Administrator.
)

echo.
pause 