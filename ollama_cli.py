#!/usr/bin/env python3
"""
Ollama CLI - Interactive command-line interface for Ollama Manager
"""

import argparse
import sys
import json
from ollama_manager import OllamaManager, CommandExecutor, APIConnector


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Ollama Model Manager CLI - Efficient model management with API and command execution'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List models
    list_parser = subparsers.add_parser('list', help='List available models')
    list_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    # Pull model
    pull_parser = subparsers.add_parser('pull', help='Download a model')
    pull_parser.add_argument('model', help='Model name to pull')
    
    # Switch model
    switch_parser = subparsers.add_parser('switch', help='Switch active model')
    switch_parser.add_argument('model', help='Model name to switch to')
    
    # Run inference
    run_parser = subparsers.add_parser('run', help='Run inference with a model')
    run_parser.add_argument('model', help='Model name')
    run_parser.add_argument('prompt', help='Prompt text')
    run_parser.add_argument('--no-stream', action='store_true', help='Disable streaming')
    
    # Delete model
    delete_parser = subparsers.add_parser('delete', help='Delete a model')
    delete_parser.add_argument('model', help='Model name to delete')
    
    # Show model info
    info_parser = subparsers.add_parser('info', help='Show model information')
    info_parser.add_argument('model', help='Model name')
    
    # Execute command
    exec_parser = subparsers.add_parser('exec', help='Execute a Linux command')
    exec_parser.add_argument('command', help='Command to execute')
    exec_parser.add_argument('--timeout', type=int, default=30, help='Timeout in seconds')
    
    # API operations
    api_parser = subparsers.add_parser('api', help='API operations')
    api_subparsers = api_parser.add_subparsers(dest='api_command', help='API commands')
    
    # API generate
    api_gen = api_subparsers.add_parser('generate', help='Generate text via API')
    api_gen.add_argument('model', help='Model name')
    api_gen.add_argument('prompt', help='Prompt text')
    
    # API chat
    api_chat = api_subparsers.add_parser('chat', help='Chat via API')
    api_chat.add_argument('model', help='Model name')
    api_chat.add_argument('message', help='Message text')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Show system status')
    
    # Start service
    start_parser = subparsers.add_parser('start', help='Start Ollama service')
    
    # Log level
    parser.add_argument('--log-level', default='INFO', 
                       choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       help='Logging level')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Initialize manager
    manager = OllamaManager(log_level=args.log_level)
    
    # Handle commands
    if args.command == 'list':
        models = manager.list_models()
        if args.json:
            print(json.dumps(models, indent=2))
        else:
            print("\nAvailable Models:")
            print("-" * 60)
            for model in models:
                print(f"Name: {model['name']}")
                print(f"  Size: {model.get('size', 'unknown')}")
                print(f"  Modified: {model.get('modified', 'unknown')}")
                print()
        return 0
        
    elif args.command == 'pull':
        print(f"Pulling model: {args.model}")
        success = manager.pull_model(args.model)
        return 0 if success else 1
        
    elif args.command == 'switch':
        success = manager.switch_model(args.model)
        if success:
            print(f"Switched to model: {args.model}")
            return 0
        return 1
        
    elif args.command == 'run':
        response = manager.run_inference(
            args.prompt, 
            model=args.model,
            stream=not args.no_stream
        )
        if not args.no_stream:
            # Already printed during streaming
            pass
        elif response:
            print(response)
        return 0 if response else 1
        
    elif args.command == 'delete':
        success = manager.delete_model(args.model)
        if success:
            print(f"Deleted model: {args.model}")
            return 0
        return 1
        
    elif args.command == 'info':
        info = manager.get_model_info(args.model)
        if info:
            print(f"\nModel Information: {args.model}")
            print("-" * 60)
            print(info['details'])
            return 0
        return 1
        
    elif args.command == 'exec':
        executor = CommandExecutor()
        result = executor.execute(args.command, timeout=args.timeout)
        
        print("STDOUT:")
        print(result['stdout'])
        
        if result['stderr']:
            print("\nSTDERR:")
            print(result['stderr'])
            
        return result['returncode']
        
    elif args.command == 'api':
        api = APIConnector()
        
        if args.api_command == 'generate':
            result = api.generate(args.model, args.prompt)
            if result:
                print(json.dumps(result, indent=2))
                return 0
            return 1
            
        elif args.api_command == 'chat':
            messages = [{'role': 'user', 'content': args.message}]
            result = api.chat(args.model, messages)
            if result:
                print(json.dumps(result, indent=2))
                return 0
            return 1
            
    elif args.command == 'status':
        print("\nOllama System Status")
        print("=" * 60)
        
        is_running = manager.check_ollama_running()
        print(f"Service Status: {'Running' if is_running else 'Not Running'}")
        
        models = manager.list_models()
        print(f"Available Models: {len(models)}")
        
        if manager.current_model:
            print(f"Current Model: {manager.current_model}")
        else:
            print("Current Model: None")
            
        # Get system resources
        executor = CommandExecutor()
        result = executor.execute("free -h")
        if result['returncode'] == 0:
            print("\nMemory Status:")
            print(result['stdout'])
            
        return 0
        
    elif args.command == 'start':
        print("Starting Ollama service...")
        success = manager.start_ollama_service()
        if success:
            print("Ollama service started successfully")
            return 0
        else:
            print("Failed to start Ollama service")
            return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
