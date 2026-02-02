#!/usr/bin/env python3
"""
Ollama Model Manager
A comprehensive system for managing Ollama models efficiently with:
- Model switching and management
- Linux command execution
- API connectivity
- Performance optimization
"""

import subprocess
import json
import os
import logging
from typing import Optional, Dict, List, Any
from datetime import datetime


class OllamaManager:
    """Main class for managing Ollama models and operations."""
    
    def __init__(self, log_level: str = "INFO"):
        """
        Initialize the Ollama Manager.
        
        Args:
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        """
        self.current_model = None
        self.available_models = []
        self.setup_logging(log_level)
        self.logger.info("Ollama Manager initialized")
        
    def setup_logging(self, level: str):
        """Configure logging for the manager."""
        logging.basicConfig(
            level=getattr(logging, level.upper()),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
    def check_ollama_running(self) -> bool:
        """Check if Ollama service is running."""
        try:
            result = subprocess.run(
                ["pgrep", "-f", "ollama"],
                capture_output=True,
                text=True,
                timeout=5
            )
            is_running = result.returncode == 0
            self.logger.debug(f"Ollama service running: {is_running}")
            return is_running
        except Exception as e:
            self.logger.error(f"Error checking Ollama service: {e}")
            return False
            
    def start_ollama_service(self) -> bool:
        """Start the Ollama service if not running."""
        if self.check_ollama_running():
            self.logger.info("Ollama service already running")
            return True
            
        try:
            self.logger.info("Starting Ollama service...")
            subprocess.Popen(
                ["ollama", "serve"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                start_new_session=True
            )
            # Give it a moment to start
            import time
            time.sleep(2)
            return self.check_ollama_running()
        except Exception as e:
            self.logger.error(f"Failed to start Ollama service: {e}")
            return False
            
    def list_models(self) -> List[Dict[str, Any]]:
        """
        List all available Ollama models.
        
        Returns:
            List of model information dictionaries
        """
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                self.logger.error(f"Failed to list models: {result.stderr}")
                return []
                
            # Parse the output
            lines = result.stdout.strip().split('\n')
            models = []
            
            if len(lines) > 1:  # Skip header
                for line in lines[1:]:
                    parts = line.split()
                    if parts:
                        models.append({
                            'name': parts[0],
                            'id': parts[1] if len(parts) > 1 else '',
                            'size': parts[2] if len(parts) > 2 else '',
                            'modified': ' '.join(parts[3:]) if len(parts) > 3 else ''
                        })
            
            self.available_models = models
            self.logger.info(f"Found {len(models)} models")
            return models
            
        except Exception as e:
            self.logger.error(f"Error listing models: {e}")
            return []
            
    def pull_model(self, model_name: str) -> bool:
        """
        Download a model from Ollama library.
        
        Args:
            model_name: Name of the model to pull
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.logger.info(f"Pulling model: {model_name}")
            result = subprocess.run(
                ["ollama", "pull", model_name],
                capture_output=True,
                text=True,
                timeout=600  # 10 minutes timeout for large models
            )
            
            if result.returncode == 0:
                self.logger.info(f"Successfully pulled model: {model_name}")
                self.list_models()  # Refresh model list
                return True
            else:
                self.logger.error(f"Failed to pull model: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error pulling model: {e}")
            return False
            
    def switch_model(self, model_name: str) -> bool:
        """
        Switch to a different model.
        
        Args:
            model_name: Name of the model to switch to
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Verify model exists
            models = self.list_models()
            model_names = [m['name'] for m in models]
            
            if model_name not in model_names:
                self.logger.warning(f"Model {model_name} not found. Available: {model_names}")
                return False
                
            self.current_model = model_name
            self.logger.info(f"Switched to model: {model_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error switching model: {e}")
            return False
            
    def run_inference(self, prompt: str, model: Optional[str] = None, 
                     stream: bool = True) -> Optional[str]:
        """
        Run inference with the current or specified model.
        
        Args:
            prompt: The prompt to send to the model
            model: Model name (uses current_model if not specified)
            stream: Whether to stream the response
            
        Returns:
            Model response or None if error
        """
        target_model = model or self.current_model
        
        if not target_model:
            self.logger.error("No model selected")
            return None
            
        try:
            self.logger.info(f"Running inference with {target_model}")
            cmd = ["ollama", "run", target_model, prompt]
            
            if stream:
                # Stream output in real-time
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                output = []
                for line in process.stdout:
                    print(line, end='')
                    output.append(line)
                    
                process.wait()
                return ''.join(output)
            else:
                # Get complete output
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                
                if result.returncode == 0:
                    return result.stdout
                else:
                    self.logger.error(f"Inference failed: {result.stderr}")
                    return None
                    
        except Exception as e:
            self.logger.error(f"Error during inference: {e}")
            return None
            
    def delete_model(self, model_name: str) -> bool:
        """
        Delete a model to free up space.
        
        Args:
            model_name: Name of the model to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.logger.info(f"Deleting model: {model_name}")
            result = subprocess.run(
                ["ollama", "rm", model_name],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                self.logger.info(f"Successfully deleted model: {model_name}")
                if self.current_model == model_name:
                    self.current_model = None
                self.list_models()  # Refresh model list
                return True
            else:
                self.logger.error(f"Failed to delete model: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error deleting model: {e}")
            return False
            
    def get_model_info(self, model_name: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific model.
        
        Args:
            model_name: Name of the model
            
        Returns:
            Dictionary with model information or None
        """
        try:
            result = subprocess.run(
                ["ollama", "show", model_name],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                # Parse output into structured data
                info = {
                    'name': model_name,
                    'details': result.stdout,
                    'timestamp': datetime.now().isoformat()
                }
                return info
            else:
                self.logger.error(f"Failed to get model info: {result.stderr}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error getting model info: {e}")
            return None


class CommandExecutor:
    """Execute Linux commands safely."""
    
    def __init__(self, allowed_commands: Optional[List[str]] = None):
        """
        Initialize command executor.
        
        Args:
            allowed_commands: List of allowed command prefixes for safety
        """
        self.logger = logging.getLogger(__name__)
        self.allowed_commands = allowed_commands or [
            'ls', 'cat', 'grep', 'find', 'ps', 'top', 'df', 
            'du', 'free', 'nvidia-smi', 'htop', 'echo', 'pwd'
        ]
        
    def execute(self, command: str, timeout: int = 30) -> Dict[str, Any]:
        """
        Execute a Linux command safely.
        
        Args:
            command: Command string to execute
            timeout: Timeout in seconds
            
        Returns:
            Dictionary with stdout, stderr, and returncode
        """
        # Safety check
        cmd_parts = command.split()
        if not cmd_parts:
            return {
                'stdout': '',
                'stderr': 'Empty command',
                'returncode': 1
            }
            
        base_cmd = cmd_parts[0]
        if base_cmd not in self.allowed_commands:
            self.logger.warning(f"Command '{base_cmd}' not in allowed list")
            return {
                'stdout': '',
                'stderr': f"Command '{base_cmd}' not allowed. Allowed: {self.allowed_commands}",
                'returncode': 1
            }
            
        try:
            self.logger.info(f"Executing command: {command}")
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            return {
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
            
        except subprocess.TimeoutExpired:
            self.logger.error(f"Command timed out: {command}")
            return {
                'stdout': '',
                'stderr': 'Command timed out',
                'returncode': 124
            }
        except Exception as e:
            self.logger.error(f"Error executing command: {e}")
            return {
                'stdout': '',
                'stderr': str(e),
                'returncode': 1
            }


class APIConnector:
    """Handle API connections and requests."""
    
    def __init__(self):
        """Initialize API connector."""
        self.logger = logging.getLogger(__name__)
        self.base_url = "http://localhost:11434"  # Default Ollama API
        
    def set_base_url(self, url: str):
        """Set the base URL for API requests."""
        self.base_url = url
        self.logger.info(f"API base URL set to: {url}")
        
    def generate(self, model: str, prompt: str, 
                options: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Call the Ollama API generate endpoint.
        
        Args:
            model: Model name
            prompt: Prompt text
            options: Optional parameters for generation
            
        Returns:
            API response as dictionary or None
        """
        try:
            import requests
        except ImportError:
            self.logger.error("requests library not installed. Install with: pip install requests")
            return None
            
        try:
            url = f"{self.base_url}/api/generate"
            payload = {
                'model': model,
                'prompt': prompt,
                'stream': False
            }
            
            if options:
                payload['options'] = options
                
            self.logger.info(f"Calling API: {url}")
            response = requests.post(url, json=payload, timeout=300)
            
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f"API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error calling API: {e}")
            return None
            
    def list_models_api(self) -> Optional[List[Dict[str, Any]]]:
        """
        Get list of models via API.
        
        Returns:
            List of model dictionaries or None
        """
        try:
            import requests
        except ImportError:
            self.logger.error("requests library not installed")
            return None
            
        try:
            url = f"{self.base_url}/api/tags"
            self.logger.info(f"Calling API: {url}")
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('models', [])
            else:
                self.logger.error(f"API error: {response.status_code}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error calling API: {e}")
            return None
            
    def chat(self, model: str, messages: List[Dict[str, str]]) -> Optional[Dict[str, Any]]:
        """
        Call the Ollama API chat endpoint.
        
        Args:
            model: Model name
            messages: List of message dictionaries with 'role' and 'content'
            
        Returns:
            API response or None
        """
        try:
            import requests
        except ImportError:
            self.logger.error("requests library not installed")
            return None
            
        try:
            url = f"{self.base_url}/api/chat"
            payload = {
                'model': model,
                'messages': messages,
                'stream': False
            }
            
            self.logger.info(f"Calling chat API: {url}")
            response = requests.post(url, json=payload, timeout=300)
            
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f"API error: {response.status_code}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error calling chat API: {e}")
            return None


if __name__ == "__main__":
    # Example usage
    print("Ollama Manager - Example Usage")
    print("=" * 50)
    
    manager = OllamaManager()
    
    print("\n1. Checking Ollama service...")
    if not manager.check_ollama_running():
        print("Starting Ollama service...")
        manager.start_ollama_service()
    
    print("\n2. Listing available models...")
    models = manager.list_models()
    for model in models:
        print(f"  - {model['name']} ({model.get('size', 'unknown')})")
    
    print("\n3. Command Executor example...")
    executor = CommandExecutor()
    result = executor.execute("echo 'Hello from Ollama Manager'")
    print(f"  Output: {result['stdout'].strip()}")
    
    print("\n4. API Connector example...")
    api = APIConnector()
    api_models = api.list_models_api()
    if api_models:
        print(f"  Found {len(api_models)} models via API")
    
    print("\nSystem ready!")
