#!/usr/bin/env python
"""
Simple run script to execute the DataLoader test.
"""
import subprocess
import sys

def main():
    """Run the DataLoader test script."""
    print("Running DataLoader test...")
    result = subprocess.run([sys.executable, "test_data_loader.py"], 
                           capture_output=True, 
                           text=True)
    
    print("\n===== STDOUT =====")
    print(result.stdout)
    
    if result.stderr:
        print("\n===== STDERR =====")
        print(result.stderr)
    
    print("\n===== TEST COMPLETED =====")
    return result.returncode

if __name__ == "__main__":
    sys.exit(main()) 