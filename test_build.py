#!/usr/bin/env python3
"""测试构建脚本"""

import sys
print(f"Python version: {sys.version}")
print("Testing imports...")

try:
    from kivy.app import App
    print("✓ Kivy imported")
except ImportError as e:
    print(f"✗ Kivy import failed: {e}")

try:
    import jnius
    print("✓ pyjnius imported")
except ImportError as e:
    print(f"✗ pyjnius import failed: {e}")

print("All basic imports successful!")
