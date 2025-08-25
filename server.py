#!/usr/bin/env python3
"""
ADB MCP Server - Android Debug Bridge Model Context Protocol Server

A comprehensive MCP server for Android device management providing:
- Device management (list, info)
- Application management (install, uninstall, list)
- File transfer (push, pull, list)
- System information (battery, memory, storage)
- Screen operations (screenshot, recording)
- Input simulation (text, tap, swipe, keys)
- Logging and debugging

Usage:
    python server.py

Requirements:
    - Python 3.10+
    - Android SDK platform-tools (adb command)
    - Connected Android device with USB debugging enabled
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from fastmcp_server import main

if __name__ == "__main__":
    main()
