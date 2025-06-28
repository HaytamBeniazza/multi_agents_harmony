"""
Interfaces Module - User Interface Components

Contains web and CLI interfaces for interacting with the AI agent system.
"""

from .web.app import app
from .cli.demo import main as run_demo

__all__ = ["app", "run_demo"]
 