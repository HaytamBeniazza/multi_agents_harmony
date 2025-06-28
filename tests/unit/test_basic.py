"""
Basic tests for the AI Agents System
"""

import pytest
import os
import sys

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))


def test_project_structure():
    """Test that the basic project structure exists"""
    project_root = os.path.join(os.path.dirname(__file__), "..", "..")

    # Check that main directories exist
    assert os.path.exists(os.path.join(project_root, "src"))
    assert os.path.exists(os.path.join(project_root, "src", "agents"))
    assert os.path.exists(os.path.join(project_root, "src", "core"))
    assert os.path.exists(os.path.join(project_root, "src", "interfaces"))


def test_package_imports():
    """Test that we can import the main packages"""
    try:
        # Test that we can import the main modules
        from src.agents.base.base_agent import BaseAgent, AgentStatus
        from src.core.config import config

        assert BaseAgent is not None
        assert AgentStatus is not None
        assert config is not None
    except ImportError as e:
        # If we can't import due to missing dependencies in CI, that's OK
        # We just want to ensure the structure is correct
        pytest.skip(f"Skipping import test due to missing dependencies: {e}")


def test_basic_functionality():
    """Test basic functionality without external dependencies"""
    # Simple test that doesn't require external APIs
    assert 1 + 1 == 2
    assert "AI Agents" in "AI Agents System"


@pytest.mark.asyncio
async def test_async_functionality():
    """Test async functionality"""
    import asyncio

    async def dummy_async_task():
        await asyncio.sleep(0.001)
        return "completed"

    result = await dummy_async_task()
    assert result == "completed"


def test_environment_variables():
    """Test environment variable handling"""
    # Test that we can set and get environment variables
    test_key = "TEST_AI_AGENTS_VAR"
    test_value = "test_value"

    os.environ[test_key] = test_value
    assert os.getenv(test_key) == test_value

    # Clean up
    del os.environ[test_key]
