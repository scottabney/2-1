#!/usr/bin/env python3
"""
Test suite for Ollama Manager System
Run with: python3 test_system.py
"""

import unittest
import sys
import os
import subprocess
from unittest.mock import Mock, patch, MagicMock
from io import StringIO

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ollama_manager import OllamaManager, CommandExecutor, APIConnector
from config_manager import ConfigManager


class TestOllamaManager(unittest.TestCase):
    """Test cases for OllamaManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.manager = OllamaManager(log_level="ERROR")
    
    def test_initialization(self):
        """Test manager initialization."""
        self.assertIsNotNone(self.manager)
        self.assertIsNone(self.manager.current_model)
        self.assertEqual(self.manager.available_models, [])
    
    @patch('subprocess.run')
    def test_check_ollama_running(self, mock_run):
        """Test Ollama service check."""
        # Service running
        mock_run.return_value = Mock(returncode=0)
        self.assertTrue(self.manager.check_ollama_running())
        
        # Service not running
        mock_run.return_value = Mock(returncode=1)
        self.assertFalse(self.manager.check_ollama_running())
    
    def test_switch_model_validation(self):
        """Test model switching with validation."""
        # Test with empty model list
        result = self.manager.switch_model("nonexistent")
        self.assertFalse(result)
    
    @patch('subprocess.run')
    def test_list_models_parsing(self, mock_run):
        """Test model list parsing."""
        mock_output = """NAME                SIZE      MODIFIED
llama2:latest       3.8 GB    2 days ago
mistral:latest      4.1 GB    1 week ago"""
        
        mock_run.return_value = Mock(
            returncode=0,
            stdout=mock_output,
            stderr=""
        )
        
        models = self.manager.list_models()
        self.assertEqual(len(models), 2)
        self.assertEqual(models[0]['name'], 'llama2:latest')


class TestCommandExecutor(unittest.TestCase):
    """Test cases for CommandExecutor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.executor = CommandExecutor()
    
    def test_initialization(self):
        """Test executor initialization."""
        self.assertIsNotNone(self.executor)
        self.assertIsNotNone(self.executor.allowed_commands)
    
    def test_command_whitelist(self):
        """Test command whitelist validation."""
        # Allowed command
        result = self.executor.execute("echo test")
        self.assertIn('stdout', result)
        self.assertIn('stderr', result)
        self.assertIn('returncode', result)
        
        # Disallowed command
        result = self.executor.execute("rm -rf /")
        self.assertEqual(result['returncode'], 1)
        self.assertIn('not allowed', result['stderr'])
    
    def test_empty_command(self):
        """Test empty command handling."""
        result = self.executor.execute("")
        self.assertEqual(result['returncode'], 1)
        self.assertIn('Empty command', result['stderr'])
    
    @patch('subprocess.run')
    def test_command_timeout(self, mock_run):
        """Test command timeout handling."""
        mock_run.side_effect = subprocess.TimeoutExpired(cmd='ls', timeout=1)
        result = self.executor.execute("ls", timeout=1)
        self.assertEqual(result['returncode'], 124)
        self.assertIn('timed out', result['stderr'])


class TestAPIConnector(unittest.TestCase):
    """Test cases for APIConnector class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.api = APIConnector()
    
    def test_initialization(self):
        """Test API connector initialization."""
        self.assertIsNotNone(self.api)
        self.assertEqual(self.api.base_url, "http://localhost:11434")
    
    def test_set_base_url(self):
        """Test setting base URL."""
        new_url = "http://example.com:8080"
        self.api.set_base_url(new_url)
        self.assertEqual(self.api.base_url, new_url)
    
    def test_api_without_requests(self):
        """Test API methods when requests is not available."""
        with patch.dict('sys.modules', {'requests': None}):
            result = self.api.list_models_api()
            self.assertIsNone(result)


class TestConfigManager(unittest.TestCase):
    """Test cases for ConfigManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Use a test config file
        self.test_config_path = "/tmp/test_config.json"
        self.config = ConfigManager(config_path=self.test_config_path)
    
    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.test_config_path):
            os.remove(self.test_config_path)
    
    def test_default_config(self):
        """Test default configuration."""
        config = self.config.get_default_config()
        self.assertIn('ollama', config)
        self.assertIn('commands', config)
        self.assertIn('logging', config)
    
    def test_get_set_config(self):
        """Test getting and setting config values."""
        # Set a value
        self.config.set('test.key', 'test_value')
        
        # Get the value
        value = self.config.get('test.key')
        self.assertEqual(value, 'test_value')
    
    def test_nested_config_keys(self):
        """Test nested configuration keys."""
        value = self.config.get('ollama.api_url')
        self.assertIsNotNone(value)
        
        # Test non-existent key with default
        value = self.config.get('nonexistent.key', 'default')
        self.assertEqual(value, 'default')


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system."""
    
    def test_system_components(self):
        """Test that all components can be initialized."""
        manager = OllamaManager(log_level="ERROR")
        executor = CommandExecutor()
        api = APIConnector()
        config = ConfigManager(config_path="/tmp/test_integration.json")
        
        self.assertIsNotNone(manager)
        self.assertIsNotNone(executor)
        self.assertIsNotNone(api)
        self.assertIsNotNone(config)
        
        # Cleanup
        if os.path.exists("/tmp/test_integration.json"):
            os.remove("/tmp/test_integration.json")
    
    def test_command_executor_with_real_command(self):
        """Test command executor with a real, safe command."""
        executor = CommandExecutor()
        result = executor.execute("echo 'test'")
        
        self.assertEqual(result['returncode'], 0)
        self.assertIn('test', result['stdout'])


def run_tests():
    """Run all tests and return results."""
    print("=" * 70)
    print("Ollama Manager System - Test Suite")
    print("=" * 70)
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestOllamaManager))
    suite.addTests(loader.loadTestsFromTestCase(TestCommandExecutor))
    suite.addTests(loader.loadTestsFromTestCase(TestAPIConnector))
    suite.addTests(loader.loadTestsFromTestCase(TestConfigManager))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print()
    print("=" * 70)
    print("Test Summary")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 70)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
