@echo off
echo ==========================================
echo Edexcel Maths Homework Tool - Setup
echo ==========================================
echo.

REM Check Python version
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://www.python.org/
    pause
    exit /b 1
)

echo Found Python:
python --version
echo.

REM Create virtual environment
echo Step 1: Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

REM Activate virtual environment
echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Step 3: Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

REM Install Playwright browsers
echo Step 4: Installing Playwright browsers...
playwright install chromium
if errorlevel 1 (
    echo WARNING: Playwright browser installation may have failed
    echo Try running: playwright install chromium
)

REM Create output directory
echo Step 5: Creating output directory...
if not exist "outputs" mkdir outputs

echo.
echo ==========================================
echo Setup Complete!
echo ==========================================
echo.
echo To use the tool:
echo   1. Activate the environment: venv\Scripts\activate
echo   2. Run: python main.py --help
echo.
echo Quick example:
echo   python main.py generate "pythagoras" -n 10 -p 3
echo.
echo Or use interactive mode:
echo   python main.py interactive
echo.

pause
