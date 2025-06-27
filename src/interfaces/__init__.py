"""
Interfaces Module - User Interface Components

Contains web and CLI interfaces for interacting with the AI agent system.
"""

from .web.app import create_app
from .cli.demo import main as run_demo

__all__ = ["create_app", "run_demo"]
