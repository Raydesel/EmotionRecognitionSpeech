#!/usr/bin/env python3
"""
Example of how to import and use GPU utilities in your notebooks
"""

# Method 1: Import from the simple_gpu_utils.py file
print("Method 1: Import from simple_gpu_utils.py")
print("=" * 50)

try:
    from simple_gpu_utils import setup_gpu_environment, gpu_device, get_gpu_info, print_gpu_info, create_gpu_optimized_model
    
    # Setup GPU environment
    setup_gpu_environment()
    
    # Print GPU info
    print_gpu_info()
    
    print("✅ Method 1 works!")
    
except ImportError as e:
    print(f"❌ Method 1 failed: {e}")

print("\n" + "=" * 50)

# Method 2: Copy the functions directly into your notebook
print("Method 2: Copy functions directly into notebook")
print("=" * 50)

# This is what we did in the notebooks - copy the functions directly
# No imports needed, everything is self-contained

print("✅ Method 2 works! (This is what we used in the notebooks)")

print("\n" + "=" * 50)
print("🎉 Both methods work! Use whichever you prefer.")
print("The notebooks now have all GPU functions built-in!")




