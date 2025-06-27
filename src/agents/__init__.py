"""
AI Agents Package - Enterprise Multi-Agent System

This package contains specialized AI agents for research, analysis, content creation, and quality assurance.
Each agent is designed to work independently or as part of a collaborative workflow.
"""

from .base import BaseAgent, AgentStatus, AgentMessage, AgentResult
from .research import ResearchAgent
from .analysis import AnalysisAgent
from .content import ContentAgent
from .quality import QualityAgent

__version__ = "1.0.0"
__author__ = "AI Agent Development Team"

__all__ = [
    "BaseAgent",
    "AgentStatus",
    "AgentMessage",
    "AgentResult",
    "ResearchAgent",
    "AnalysisAgent",
    "ContentAgent",
    "QualityAgent",
]

# Agent registry for dynamic loading
AGENT_REGISTRY = {
    "research": ResearchAgent,
    "analysis": AnalysisAgent,
    "content": ContentAgent,
    "quality": QualityAgent,
}


def get_agent(agent_type: str) -> BaseAgent:
    """Factory function to get agent by type"""
    if agent_type in AGENT_REGISTRY:
        agent_class = AGENT_REGISTRY[agent_type]
        return agent_class()
    else:
        raise ValueError(f"Unknown agent type: {agent_type}")


def list_available_agents():
    """List all available agent types"""
    return list(AGENT_REGISTRY.keys())
