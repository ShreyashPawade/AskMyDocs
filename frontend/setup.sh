#!/bin/bash

# AskMyDocs Frontend Setup Script
# Automates environment setup and dependency installation

set -e

echo "🚀 AskMyDocs Frontend Setup"
echo "======================================"
echo ""

# Check Python version
echo "✓ Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "  Python version: $PYTHON_VERSION"
echo ""

# Create virtual environment
echo "✓ Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "  Virtual environment created."
else
    echo "  Virtual environment already exists."
fi

# Activate virtual environment
echo "✓ Activating virtual environment..."
source venv/bin/activate
echo ""

# Upgrade pip
echo "✓ Upgrading pip..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
echo ""

# Install dependencies
echo "✓ Installing dependencies..."
pip install -r requirements.txt
echo ""

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "✓ Creating .env file..."
    cp .env.example .env
    echo "  .env file created. Update BACKEND_URL if needed."
else
    echo "✓ .env file already exists."
fi
echo ""

# Create .streamlit directory if it doesn't exist
if [ ! -d ".streamlit" ]; then
    echo "✓ Creating .streamlit directory..."
    mkdir -p .streamlit
fi
echo ""

# Print next steps
echo "======================================"
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Ensure the backend server is running:"
echo "   FastAPI backend should be at: http://localhost:8000"
echo ""
echo "2. Update .env if using a different backend URL"
echo ""
echo "3. Start the frontend:"
echo "   streamlit run streamlit_app.py"
echo ""
echo "4. Open your browser to:"
echo "   http://localhost:8501"
echo ""
echo "======================================"
