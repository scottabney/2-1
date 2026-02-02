# Ollama Model Management System

A comprehensive, efficient system for managing Ollama models on Linux with advanced features including model switching, Linux command execution, and API connectivity.

## Features

- 🚀 **Efficient Model Management**: Seamlessly pull, switch, and manage multiple Ollama models
- 🔄 **Dynamic Model Switching**: Quickly switch between models without service restarts
- 💻 **Linux Command Execution**: Safely execute system commands with configurable permissions
- 🌐 **API Connectivity**: Full REST API support for programmatic access
- 📊 **Performance Optimization**: Optimized for efficient resource usage
- 🔧 **Configuration Management**: Flexible configuration system for customization
- 📝 **Comprehensive Logging**: Detailed logging for debugging and monitoring

## Installation

### Prerequisites

- Python 3.8 or higher
- Ollama installed on your Linux system
- pip (Python package manager)

### Install Ollama

If you haven't installed Ollama yet:

```bash
curl https://ollama.ai/install.sh | sh
```

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Quick Start

### 1. Using the CLI

The easiest way to interact with the system:

```bash
# Make CLI executable
chmod +x ollama_cli.py

# Check system status
./ollama_cli.py status

# Start Ollama service (if not running)
./ollama_cli.py start

# List available models
./ollama_cli.py list

# Pull a model
./ollama_cli.py pull llama2

# Run inference
./ollama_cli.py run llama2 "What is machine learning?"

# Execute system commands
./ollama_cli.py exec "df -h"

# Get model information
./ollama_cli.py info llama2
```

### 2. Using Python API

```python
from ollama_manager import OllamaManager, CommandExecutor, APIConnector

# Initialize manager
manager = OllamaManager(log_level="INFO")

# Start service if needed
if not manager.check_ollama_running():
    manager.start_ollama_service()

# List models
models = manager.list_models()

# Pull a new model
manager.pull_model("llama2")

# Switch to a model
manager.switch_model("llama2")

# Run inference
response = manager.run_inference("Explain quantum computing")

# Execute commands
executor = CommandExecutor()
result = executor.execute("free -h")

# Use API
api = APIConnector()
result = api.generate("llama2", "Hello, world!")
```

## Components

### 1. OllamaManager

Core class for managing Ollama models:

- `check_ollama_running()`: Check if Ollama service is active
- `start_ollama_service()`: Start the Ollama service
- `list_models()`: Get all available models
- `pull_model(model_name)`: Download a new model
- `switch_model(model_name)`: Switch active model
- `run_inference(prompt, model)`: Run inference
- `delete_model(model_name)`: Remove a model
- `get_model_info(model_name)`: Get detailed model information

### 2. CommandExecutor

Safe Linux command execution:

- Whitelist-based command filtering
- Timeout protection
- Structured output (stdout, stderr, returncode)

```python
executor = CommandExecutor(allowed_commands=['ls', 'df', 'free'])
result = executor.execute("ls -la")
```

### 3. APIConnector

REST API operations:

- `generate(model, prompt)`: Generate text
- `chat(model, messages)`: Chat conversation
- `list_models_api()`: List models via API

### 4. ConfigManager

Configuration management:

```python
from config_manager import ConfigManager

config = ConfigManager()
config.set('ollama.default_model', 'llama2')
```

## Configuration

The system uses a `config.json` file for customization:

```json
{
  "ollama": {
    "api_url": "http://localhost:11434",
    "default_model": "llama2",
    "auto_start_service": true,
    "timeout": 300
  },
  "commands": {
    "allowed": ["ls", "cat", "grep", "find", "ps", "df", "du", "free"],
    "timeout": 30
  },
  "logging": {
    "level": "INFO"
  },
  "performance": {
    "gpu_layers": -1,
    "context_size": 2048,
    "batch_size": 512
  }
}
```

## Examples

Run the provided examples:

```bash
# Basic operations
python3 example_basic.py

# API operations
python3 example_api.py

# Command execution
python3 example_commands.py
```

## CLI Commands Reference

### Model Management
- `list`: List all available models
- `pull <model>`: Download a model
- `switch <model>`: Switch active model
- `delete <model>`: Delete a model
- `info <model>`: Show model details

### Inference
- `run <model> <prompt>`: Run inference
- `run <model> <prompt> --no-stream`: Disable streaming output

### System Operations
- `status`: Show system status
- `start`: Start Ollama service
- `exec <command>`: Execute Linux command

### API Operations
- `api generate <model> <prompt>`: Generate via API
- `api chat <model> <message>`: Chat via API

## Performance Optimization

The system includes several optimizations:

1. **GPU Acceleration**: Automatically uses GPU if available
2. **Efficient Model Switching**: Fast context switching between models
3. **Streaming Output**: Real-time response streaming
4. **Resource Monitoring**: Built-in system resource checks

## Security

- Command whitelist prevents arbitrary command execution
- Timeout protection for all operations
- Configurable security policies

## Troubleshooting

### Ollama service not starting
```bash
# Check if Ollama is installed
which ollama

# Try starting manually
ollama serve
```

### API requests failing
```bash
# Install requests library
pip install requests

# Check if service is running on correct port
curl http://localhost:11434/api/tags
```

### Permission errors
```bash
# Make scripts executable
chmod +x ollama_cli.py example_*.py
```

## Architecture

```
┌─────────────────────────────────────────┐
│         Ollama CLI Interface            │
├─────────────────────────────────────────┤
│         OllamaManager (Core)            │
│  - Model Management                     │
│  - Service Control                      │
│  - Inference Engine                     │
├──────────────┬──────────────────────────┤
│ Command      │  API Connector           │
│ Executor     │  - REST API              │
│              │  - JSON Responses        │
└──────────────┴──────────────────────────┘
         │                │
         ▼                ▼
    Linux System    Ollama Service
```

## Contributing

Contributions are welcome! Please ensure:
- Code follows existing style
- All functions have docstrings
- Examples are updated for new features

## License

MIT License - See LICENSE file for details

## Support

For issues or questions:
- Check the examples directory
- Review the troubleshooting section
- Open an issue on GitHub

## Roadmap

- [ ] Multi-model parallel processing
- [ ] Advanced caching mechanisms
- [ ] Web UI interface
- [ ] Model performance benchmarking
- [ ] Container support (Docker)
- [ ] Distributed model execution
