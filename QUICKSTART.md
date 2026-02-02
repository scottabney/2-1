# Ollama Manager System - Quick Reference Guide

## Installation
```bash
# Run setup script
chmod +x setup.sh
./setup.sh
```

## Common Commands

### System Management
```bash
# Check system status
./ollama_cli.py status

# Start Ollama service
./ollama_cli.py start
```

### Model Operations
```bash
# List available models
./ollama_cli.py list

# Pull a model (e.g., llama2, mistral, codellama)
./ollama_cli.py pull llama2

# Get model information
./ollama_cli.py info llama2

# Delete a model
./ollama_cli.py delete old-model
```

### Running Inference
```bash
# Quick inference with streaming
./ollama_cli.py run llama2 "Explain machine learning"

# Inference without streaming (wait for complete response)
./ollama_cli.py run llama2 "What is Python?" --no-stream
```

### System Commands
```bash
# Execute Linux commands safely
./ollama_cli.py exec "df -h"
./ollama_cli.py exec "free -h"
./ollama_cli.py exec "ls -la /tmp"
```

### API Operations
```bash
# Generate text via API
./ollama_cli.py api generate llama2 "Hello, AI!"

# Chat via API
./ollama_cli.py api chat llama2 "Tell me a joke"
```

## Python API Usage

### Basic Example
```python
from ollama_manager import OllamaManager

# Initialize
manager = OllamaManager()

# Start service
manager.start_ollama_service()

# List models
models = manager.list_models()

# Run inference
response = manager.run_inference("What is AI?", model="llama2")
```

### Command Execution
```python
from ollama_manager import CommandExecutor

executor = CommandExecutor()
result = executor.execute("df -h")
print(result['stdout'])
```

### API Connector
```python
from ollama_manager import APIConnector

api = APIConnector()
result = api.generate("llama2", "Explain quantum computing")
print(result['response'])
```

## Configuration

Edit `config.json` to customize:
```json
{
  "ollama": {
    "api_url": "http://localhost:11434",
    "default_model": "llama2",
    "timeout": 300
  },
  "commands": {
    "allowed": ["ls", "cat", "grep", "df", "free"],
    "timeout": 30
  }
}
```

## Examples

Run example scripts:
```bash
# Basic operations
python3 example_basic.py

# API operations
python3 example_api.py

# Command execution
python3 example_commands.py

# Advanced demo (all features)
python3 example_advanced.py
```

## Troubleshooting

### Ollama not found
```bash
curl https://ollama.ai/install.sh | sh
```

### Service won't start
```bash
# Check if already running
pgrep -f ollama

# Start manually
ollama serve
```

### API errors
```bash
# Install requests
pip install requests

# Check service
curl http://localhost:11434/api/tags
```

### Permission denied
```bash
chmod +x ollama_cli.py example_*.py
```

## Testing
```bash
# Run test suite
python3 test_system.py
```

## Architecture Overview

```
Ollama Manager System
├── ollama_manager.py      # Core manager (model operations)
├── ollama_cli.py          # Command-line interface
├── config_manager.py      # Configuration handling
├── test_system.py         # Test suite
├── setup.sh               # Setup script
├── requirements.txt       # Python dependencies
├── example_basic.py       # Basic usage example
├── example_api.py         # API usage example
├── example_commands.py    # Command execution example
├── example_advanced.py    # Complete demonstration
└── README.md              # Full documentation
```

## Key Features

✅ Efficient model management
✅ Dynamic model switching
✅ Safe command execution
✅ REST API support
✅ Configuration system
✅ Comprehensive logging
✅ Error handling
✅ Performance optimized

## Performance Tips

1. **GPU Acceleration**: Ensure nvidia-smi works for GPU support
2. **Model Size**: Smaller models = faster switching
3. **Context Size**: Adjust in config.json for memory efficiency
4. **Streaming**: Use streaming for real-time responses

## Security

- Commands are whitelisted (configurable)
- Timeouts prevent hanging processes
- Safe defaults for all operations
- No arbitrary code execution

## Getting Help

1. Check README.md for detailed documentation
2. Run examples to see usage patterns
3. Review test_system.py for code examples
4. Check logs for error details

## Useful Model Names

Common Ollama models to try:
- llama2 (7B, 13B, 70B)
- mistral
- codellama
- llama3
- neural-chat
- starling-lm

Pull with: `./ollama_cli.py pull <model-name>`
