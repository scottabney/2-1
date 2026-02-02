#!/usr/bin/env python3
"""
Example: Basic model operations with Ollama Manager
"""

from ollama_manager import OllamaManager

def main():
    print("=" * 60)
    print("Example 1: Basic Model Operations")
    print("=" * 60)
    
    # Initialize manager
    manager = OllamaManager(log_level="INFO")
    
    # Check and start service
    print("\n1. Checking Ollama service...")
    if not manager.check_ollama_running():
        print("   Service not running. Starting...")
        manager.start_ollama_service()
    else:
        print("   ✓ Service is running")
    
    # List available models
    print("\n2. Listing available models...")
    models = manager.list_models()
    if models:
        for model in models:
            print(f"   - {model['name']}: {model.get('size', 'unknown')}")
    else:
        print("   No models found. Consider pulling one:")
        print("   Example: manager.pull_model('llama2')")
    
    # Switch model (if available)
    if models:
        first_model = models[0]['name']
        print(f"\n3. Switching to model: {first_model}")
        if manager.switch_model(first_model):
            print(f"   ✓ Switched to {first_model}")
            
            # Run a simple inference
            print("\n4. Running inference...")
            prompt = "What is 2+2?"
            print(f"   Prompt: {prompt}")
            print("   Response:", end=" ")
            response = manager.run_inference(prompt, stream=False)
            if response:
                print(response.strip()[:100] + "...")
    
    print("\n" + "=" * 60)
    print("Example complete!")
    print("=" * 60)

if __name__ == '__main__':
    main()
