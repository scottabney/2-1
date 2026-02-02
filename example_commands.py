#!/usr/bin/env python3
"""
Example: Command execution with Ollama Manager
"""

from ollama_manager import CommandExecutor

def main():
    print("=" * 60)
    print("Example 3: Command Execution")
    print("=" * 60)
    
    # Initialize command executor
    executor = CommandExecutor()
    
    print("\n1. System Information Commands")
    print("-" * 60)
    
    # Execute various commands
    commands = [
        ("ls -la /tmp", "List /tmp directory"),
        ("df -h", "Disk usage"),
        ("free -h", "Memory usage"),
        ("echo 'Hello from Ollama Manager'", "Echo test")
    ]
    
    for cmd, description in commands:
        print(f"\n{description}:")
        print(f"Command: {cmd}")
        
        result = executor.execute(cmd)
        
        if result['returncode'] == 0:
            print("Output:")
            print(result['stdout'][:200])  # First 200 chars
            if len(result['stdout']) > 200:
                print("... (truncated)")
        else:
            print(f"Error: {result['stderr']}")
    
    print("\n2. Checking GPU availability...")
    result = executor.execute("nvidia-smi")
    if result['returncode'] == 0:
        print("   ✓ NVIDIA GPU detected")
        print(result['stdout'][:300])
    else:
        print("   No NVIDIA GPU detected or nvidia-smi not available")
    
    print("\n" + "=" * 60)
    print("Example complete!")
    print("=" * 60)

if __name__ == '__main__':
    main()
