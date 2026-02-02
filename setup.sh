#!/bin/bash

echo "=========================================="
echo "Edexcel Maths Homework Tool - Setup"
echo "=========================================="
echo

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.9+ first"
    exit 1
fi

echo "Found Python:"
python3 --version
echo

# Create virtual environment
echo "Step 1: Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi

# Activate virtual environment
echo "Step 2: Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Step 3: Installing Python dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

# Install Playwright browsers
echo "Step 4: Installing Playwright browsers..."
playwright install chromium
if [ $? -ne 0 ]; then
    echo "WARNING: Playwright browser installation may have failed"
    echo "Try running: playwright install chromium"
fi

# Create output directory
echo "Step 5: Creating output directory..."
mkdir -p outputs

echo
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo
echo "To use the tool:"
echo "  1. Activate the environment: source venv/bin/activate"
echo "  2. Run: python main.py --help"
echo
echo "Quick example:"
echo "  python main.py generate \"pythagoras\" -n 10 -p 3"
echo
echo "Or use interactive mode:"
echo "  python main.py interactive"
echo
