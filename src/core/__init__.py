"""
Core Module - System Components and Configuration

Contains core system components including orchestration, configuration, and utilities.
"""

from .config import config
from .orchestrator import AgentOrchestrator

__all__ = ['config', 'AgentOrchestrator'] 