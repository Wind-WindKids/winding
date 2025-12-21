#!/usr/bin/env python3
"""A shining, fancy hello world."""

import sys
from datetime import datetime


def fancy_greeting():
    """Generate a fancy greeting with style."""
    name = "World"
    if len(sys.argv) > 1:
        name = sys.argv[1]
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    greeting = f"""
╔═══════════════════════════════════════╗
║                                       ║
║   ✨ Hello, {name:25s} ✨   ║
║                                       ║
║   Time: {timestamp:29s}   ║
║                                       ║
╚═══════════════════════════════════════╝
    """
    return greeting


if __name__ == "__main__":
    print(fancy_greeting())
