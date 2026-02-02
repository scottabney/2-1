"""
Configuration management for Ollama Manager
"""

import json
import os
from typing import Dict, Any, Optional
import logging


class ConfigManager:
    """Manage configuration for Ollama system."""
    
    def __init__(self, config_path: str = "config.json"):
        """
        Initialize configuration manager.
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path
        self.logger = logging.getLogger(__name__)
        self.config = self.load_config()
        
    def load_config(self) -> Dict[str, Any]:
        """
        Load configuration from file.
        
        Returns:
            Configuration dictionary
        """
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    self.logger.info(f"Loaded config from {self.config_path}")
                    return config
            except Exception as e:
                self.logger.error(f"Error loading config: {e}")
                return self.get_default_config()
        else:
            self.logger.info("No config file found, using defaults")
            return self.get_default_config()
            
    def save_config(self) -> bool:
        """
        Save configuration to file.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
                self.logger.info(f"Saved config to {self.config_path}")
                return True
        except Exception as e:
            self.logger.error(f"Error saving config: {e}")
            return False
            
    def get_default_config(self) -> Dict[str, Any]:
        """
        Get default configuration.
        
        Returns:
            Default configuration dictionary
        """
        return {
            "ollama": {
                "api_url": "http://localhost:11434",
                "default_model": None,
                "auto_start_service": True,
                "timeout": 300
            },
            "commands": {
                "allowed": [
                    "ls", "cat", "grep", "find", "ps", "top", "df",
                    "du", "free", "nvidia-smi", "htop", "echo", "pwd"
                ],
                "timeout": 30
            },
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            },
            "performance": {
                "gpu_layers": -1,  # Use all GPU layers
                "num_threads": None,  # Auto-detect
                "context_size": 2048,
                "batch_size": 512
            }
        }
        
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            key: Configuration key (supports nested with dots)
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
                
        return value
        
    def set(self, key: str, value: Any) -> bool:
        """
        Set configuration value.
        
        Args:
            key: Configuration key (supports nested with dots)
            value: Value to set
            
        Returns:
            True if successful
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
            
        config[keys[-1]] = value
        return self.save_config()
        
    def update(self, updates: Dict[str, Any]) -> bool:
        """
        Update multiple configuration values.
        
        Args:
            updates: Dictionary of updates
            
        Returns:
            True if successful
        """
        self.config.update(updates)
        return self.save_config()
