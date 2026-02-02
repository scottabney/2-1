#!/usr/bin/env python3
"""
Example: API operations with Ollama Manager
"""

from ollama_manager import APIConnector

# Constants
MAX_DISPLAY_LENGTH = 100  # Maximum characters to display from responses

def main():
    print("=" * 60)
    print("Example 2: API Operations")
    print("=" * 60)
    
    # Initialize API connector
    api = APIConnector()
    
    # List models via API
    print("\n1. Listing models via API...")
    models = api.list_models_api()
    if models:
        print(f"   Found {len(models)} models")
        for model in models[:3]:  # Show first 3
            print(f"   - {model.get('name', 'unknown')}")
    else:
        print("   Could not fetch models. Make sure:")
        print("   - Ollama service is running")
        print("   - requests library is installed: pip install requests")
    
    # Generate text (if models available)
    if models and len(models) > 0:
        model_name = models[0]['name']
        print(f"\n2. Generating text with {model_name}...")
        
        result = api.generate(
            model=model_name,
            prompt="Explain what Ollama is in one sentence."
        )
        
        if result:
            response_text = result.get('response', 'No response')[:MAX_DISPLAY_LENGTH]
            print(f"   Response: {response_text}...")
        else:
            print("   Generation failed")
    
        # Chat example
        print(f"\n3. Chat conversation with {model_name}...")
        messages = [
            {'role': 'user', 'content': 'Hello! How are you?'}
        ]
        
        result = api.chat(model=model_name, messages=messages)
        if result:
            message = result.get('message', {})
            content_text = message.get('content', 'No content')[:MAX_DISPLAY_LENGTH]
            print(f"   Assistant: {content_text}...")
    
    print("\n" + "=" * 60)
    print("Example complete!")
    print("=" * 60)

if __name__ == '__main__':
    main()
