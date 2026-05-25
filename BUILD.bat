@echo off
REM Smart Trash Downloader EXE Builder
REM Run this script to build the EXE automatically

echo.
echo ========================================
echo  Smart Trash Downloader Builder
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/4] Checking Python version...
python --version

echo.
echo [2/4] Installing PyInstaller...
pip install --quiet pyinstaller

echo.
echo [3/4] Building EXE...
echo This may take a few minutes on first run...
pyinstaller SmartTrashDownloader.spec

echo.
echo [4/4] Build complete!
echo.
echo ========================================
echo  SUCCESS!
echo ========================================
echo.
echo Your EXE is ready at:
echo   dist\SmartTrashDownloader\SmartTrashDownloader.exe
echo.
pause
