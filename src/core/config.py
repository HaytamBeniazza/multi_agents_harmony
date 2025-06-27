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
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4-turbo-preview')
    OPENAI_TEMPERATURE = float(os.getenv('OPENAI_TEMPERATURE', '0.7'))
    
    # Web Scraping Configuration
    USER_AGENT = os.getenv('USER_AGENT', 
                          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', '30'))
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))
    
    # Agent Configuration
    MAX_RESEARCH_SOURCES = int(os.getenv('MAX_RESEARCH_SOURCES', '5'))
    MIN_CONTENT_LENGTH = int(os.getenv('MIN_CONTENT_LENGTH', '1000'))
    QUALITY_THRESHOLD = float(os.getenv('QUALITY_THRESHOLD', '0.8'))
    
    # Web Interface Configuration
    FLASK_HOST = os.getenv('FLASK_HOST', 'localhost')
    FLASK_PORT = int(os.getenv('FLASK_PORT', '5000'))
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'agent_system.log')
    
    @classmethod
    def validate_config(cls) -> Dict[str, Any]:
        """Validate configuration and return status"""
        issues = []
        
        if not cls.OPENAI_API_KEY:
            issues.append("OPENAI_API_KEY is required")
        
        if cls.OPENAI_TEMPERATURE < 0 or cls.OPENAI_TEMPERATURE > 2:
            issues.append("OPENAI_TEMPERATURE must be between 0 and 2")
        
        if cls.MAX_RESEARCH_SOURCES < 1:
            issues.append("MAX_RESEARCH_SOURCES must be at least 1")
        
        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'config': {
                'model': cls.OPENAI_MODEL,
                'temperature': cls.OPENAI_TEMPERATURE,
                'max_sources': cls.MAX_RESEARCH_SOURCES,
                'min_content_length': cls.MIN_CONTENT_LENGTH
            }
        }

# Global configuration instance
config = Config() 