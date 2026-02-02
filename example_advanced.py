#!/usr/bin/env python3
"""
Advanced example: Combined operations with Ollama Manager
Demonstrates model switching, command execution, and API operations
"""

from ollama_manager import OllamaManager, CommandExecutor, APIConnector
from config_manager import ConfigManager
import time

# Constants
SERVICE_START_DELAY_SECONDS = 2  # Time to wait for Ollama service to initialize
MAX_DISPLAY_LENGTH = 100  # Maximum characters to display from responses


def main():
    print("=" * 70)
    print("Advanced Example: Complete System Demonstration")
    print("=" * 70)
    
    # Initialize all components
    print("\n📋 Initializing components...")
    config = ConfigManager()
    manager = OllamaManager(log_level="INFO")
    executor = CommandExecutor()
    api = APIConnector()
    
    # 1. System Status Check
    print("\n" + "=" * 70)
    print("1. SYSTEM STATUS CHECK")
    print("=" * 70)
    
    print("\n🔍 Checking Ollama service...")
    if not manager.check_ollama_running():
        print("⚠️  Service not running. Starting...")
        if manager.start_ollama_service():
            print("✅ Service started successfully")
            time.sleep(SERVICE_START_DELAY_SECONDS)  # Give it time to initialize
        else:
            print("❌ Failed to start service")
            return
    else:
        print("✅ Service is running")
    
    # 2. System Resources
    print("\n🖥️  Checking system resources...")
    result = executor.execute("free -h")
    if result['returncode'] == 0:
        lines = result['stdout'].strip().split('\n')[:2]
        for line in lines:
            print(f"   {line}")
    
    # 3. Model Management
    print("\n" + "=" * 70)
    print("2. MODEL MANAGEMENT")
    print("=" * 70)
    
    print("\n📚 Available models:")
    models = manager.list_models()
    if not models:
        print("   No models found.")
        print("   💡 Tip: Pull a model with: ./ollama_cli.py pull llama2")
        return
    
    for i, model in enumerate(models, 1):
        print(f"   {i}. {model['name']}")
        print(f"      Size: {model.get('size', 'unknown')}")
        print(f"      Modified: {model.get('modified', 'unknown')}")
    
    # 4. Model Switching Demo
    if len(models) >= 1:
        print("\n" + "=" * 70)
        print("3. MODEL SWITCHING DEMONSTRATION")
        print("=" * 70)
        
        test_model = models[0]['name']
        print(f"\n🔄 Switching to model: {test_model}")
        
        if manager.switch_model(test_model):
            print(f"✅ Successfully switched to {test_model}")
            
            # Get model details
            print(f"\n📊 Model information:")
            info = manager.get_model_info(test_model)
            if info:
                details = info['details'].split('\n')[:5]
                for detail in details:
                    if detail.strip():
                        print(f"   {detail}")
        
        # 5. Quick Inference Test
        print("\n" + "=" * 70)
        print("4. INFERENCE TEST")
        print("=" * 70)
        
        test_prompt = "What is 5+7? Just give the number."
        print(f"\n💭 Testing inference with prompt: '{test_prompt}'")
        print("   Response: ", end="", flush=True)
        
        response = manager.run_inference(test_prompt, stream=False)
        if response:
            # Print first MAX_DISPLAY_LENGTH chars of response
            print(response.strip()[:MAX_DISPLAY_LENGTH])
        else:
            print("Failed to get response")
    
    # 6. API Operations
    print("\n" + "=" * 70)
    print("5. API CONNECTIVITY TEST")
    print("=" * 70)
    
    print("\n🌐 Testing API endpoints...")
    api_models = api.list_models_api()
    if api_models:
        print(f"✅ API is accessible - Found {len(api_models)} models")
    else:
        print("⚠️  API not accessible. Make sure:")
        print("   - Ollama service is running")
        print("   - requests library is installed: pip install requests")
    
    # 7. Command Execution
    print("\n" + "=" * 70)
    print("6. COMMAND EXECUTION TEST")
    print("=" * 70)
    
    print("\n⚙️  Executing system commands...")
    
    commands = [
        ("df -h /", "Disk usage"),
        ("echo 'Ollama Manager Test'", "Echo test")
    ]
    
    for cmd, desc in commands:
        print(f"\n   {desc}: {cmd}")
        result = executor.execute(cmd)
        if result['returncode'] == 0:
            output = result['stdout'].strip().split('\n')[0]
            print(f"   ✅ {output}")
        else:
            print(f"   ❌ Error: {result['stderr']}")
    
    # 8. Configuration Check
    print("\n" + "=" * 70)
    print("7. CONFIGURATION")
    print("=" * 70)
    
    print("\n⚙️  Current configuration:")
    print(f"   API URL: {config.get('ollama.api_url')}")
    print(f"   Timeout: {config.get('ollama.timeout')}s")
    print(f"   Log Level: {config.get('logging.level')}")
    print(f"   Allowed Commands: {len(config.get('commands.allowed'))} commands")
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"✅ System Status: Operational")
    print(f"✅ Models Available: {len(models)}")
    print(f"✅ Current Model: {manager.current_model or 'None'}")
    print(f"✅ API Status: {'Connected' if api_models else 'Not connected'}")
    print("\n" + "=" * 70)
    print("Advanced demonstration complete!")
    print("=" * 70)


if __name__ == '__main__':
    main()
