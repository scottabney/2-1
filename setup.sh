#!/bin/bash
# Setup script for Ollama Manager System

set -e

echo "================================"
echo "Ollama Manager System Setup"
echo "================================"

# Check Python version
echo "Checking Python version..."
python3 --version || { echo "Python 3 not found. Please install Python 3.8+"; exit 1; }

# Check if Ollama is installed
echo "Checking Ollama installation..."
if ! command -v ollama &> /dev/null; then
    echo "Ollama not found. Installing..."
    curl https://ollama.ai/install.sh | sh
else
    echo "✓ Ollama is installed"
fi

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt || { echo "Failed to install dependencies"; exit 1; }

# Make scripts executable
echo "Making scripts executable..."
chmod +x ollama_cli.py example_*.py

# Test Ollama service
echo "Testing Ollama service..."
if pgrep -f "ollama" > /dev/null; then
    echo "✓ Ollama service is running"
else
    echo "Starting Ollama service..."
    ollama serve &
    sleep 3
fi

# Create default config if it doesn't exist
if [ ! -f config.json ]; then
    echo "Creating default configuration..."
    python3 -c "from config_manager import ConfigManager; ConfigManager().save_config()"
fi

echo ""
echo "================================"
echo "Setup Complete!"
echo "================================"
echo ""
echo "Quick start:"
echo "  ./ollama_cli.py status         - Check system status"
echo "  ./ollama_cli.py list           - List models"
echo "  python3 example_basic.py       - Run basic example"
echo ""
echo "For more information, see README.md"
