"""
AI Research & Content Creation Team - Configuration Management
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration class for the AI Agent System"""

    # Google Gemini Configuration (Primary AI Provider)
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBn_YyzcsyZ7HHIvEEZ04Tu2gqnpOL-0uo")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

    # OpenAI/OpenRouter Configuration (Backup)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "openai/gpt-4-turbo-preview")
    OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))

    # AI Provider Selection
    AI_PROVIDER = os.getenv("AI_PROVIDER", "gemini")  # "gemini" or "openai"

    # Token Management - Optimized for fast responses
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "800"))  # Conservative limit for speed

    # OpenRouter specific settings
    HTTP_REFERER = os.getenv("HTTP_REFERER", "https://github.com/HaytamBeniazza/multi_agents_harmony")
    X_TITLE = os.getenv("X_TITLE", "AI Research & Content Creation Team")

    # Web Scraping Configuration
    USER_AGENT = os.getenv(
        "USER_AGENT",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    )
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))

    # Agent Configuration
    MAX_RESEARCH_SOURCES = int(os.getenv("MAX_RESEARCH_SOURCES", "3"))  # Reduced from 5
    MIN_CONTENT_LENGTH = int(os.getenv("MIN_CONTENT_LENGTH", "500"))  # Reduced from 1000
    QUALITY_THRESHOLD = float(os.getenv("QUALITY_THRESHOLD", "0.8"))

    # Web Interface Configuration
    FLASK_HOST = os.getenv("FLASK_HOST", "localhost")
    FLASK_PORT = int(os.getenv("FLASK_PORT", "5000"))
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", "True").lower() == "true"

    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "agent_system.log")

    @classmethod
    def validate_config(cls) -> Dict[str, Any]:
        """Validate configuration and return status"""
        issues = []

        if cls.AI_PROVIDER == "gemini" and not cls.GEMINI_API_KEY:
            issues.append("GEMINI_API_KEY is required when using Gemini provider")
        elif cls.AI_PROVIDER == "openai" and not cls.OPENAI_API_KEY:
            issues.append("OPENAI_API_KEY is required when using OpenAI provider")

        if cls.OPENAI_TEMPERATURE < 0 or cls.OPENAI_TEMPERATURE > 2:
            issues.append("OPENAI_TEMPERATURE must be between 0 and 2")

        if cls.MAX_RESEARCH_SOURCES < 1:
            issues.append("MAX_RESEARCH_SOURCES must be at least 1")

        if cls.MAX_TOKENS < 50 or cls.MAX_TOKENS > 4096:
            issues.append("MAX_TOKENS must be between 50 and 4096")

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "config": {
                "ai_provider": cls.AI_PROVIDER,
                "model": cls.GEMINI_MODEL if cls.AI_PROVIDER == "gemini" else cls.OPENAI_MODEL,
                "temperature": cls.OPENAI_TEMPERATURE,
                "max_tokens": cls.MAX_TOKENS,
                "max_sources": cls.MAX_RESEARCH_SOURCES,
                "min_content_length": cls.MIN_CONTENT_LENGTH,
            },
        }


# Global configuration instance
config = Config()
