#!/bin/bash

# MCP Server POC Setup Script
# This script helps set up the development environment

set -e

echo "🚀 Setting up MCP Server POC..."

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.10"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 10) else 1)"; then
    echo "❌ Python 3.10+ is required. Found: $python_version"
    exit 1
fi

echo "✅ Python version: $python_version"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Install dev dependencies (optional)
read -p "Install development dependencies? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📥 Installing development dependencies..."
    pip install -r requirements-dev.txt
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "✅ Created .env file. You can edit it to customize settings."
fi

# Run tests
read -p "Run tests? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🧪 Running tests..."
    pytest -v || echo "⚠️  Some tests failed, but setup is complete"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To get started:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run the server: python -m src.server"
echo "  3. Or run example client: python examples/example_client.py"
echo ""
echo "For more information, see README.md"

