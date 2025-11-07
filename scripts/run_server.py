#!/usr/bin/env python3
"""
Script to run the MCP server
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.server import main
import asyncio

if __name__ == "__main__":
    asyncio.run(main())

