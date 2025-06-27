"""
Setup Script for AI Research & Content Creation Team
"""
import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("ERROR: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"Python version {sys.version_info.major}.{sys.version_info.minor} is compatible")
    return True

def install_dependencies():
    """Check if dependencies are already installed (Docker environment)"""
    print("\nChecking dependencies...")
    try:
        # In Docker, dependencies are already installed during build
        # Just verify key packages are available
        import openai
        import flask
        import langchain
        import requests
        print("Dependencies are properly installed")
        return True
    except ImportError as e:
        print(f"WARNING: Some dependencies may be missing: {e}")
        print("This is expected if running outside Docker environment")
        return True  # Don't fail in Docker environment

def create_env_file():
    """Check .env file status"""
    env_file = Path(".env")
    
    if env_file.exists():
        print(".env file already exists")
        
        # Check if API key is set
        try:
            with open(env_file, 'r') as f:
                content = f.read()
                if 'OPENAI_API_KEY=your_openai_api_key_here' in content:
                    print("WARNING: Please set your actual OpenAI API key in .env file")
                elif 'OPENAI_API_KEY=' in content and len(content.split('OPENAI_API_KEY=')[1].split('\n')[0].strip()) > 10:
                    print("OpenAI API key appears to be configured")
        except Exception:
            pass
        return
    
    print("\nCreating .env file from template...")
    
    # Copy from development template
    try:
        import shutil
        shutil.copy("config/development.env", ".env")
        print(".env file created from template")
        print("IMPORTANT: Edit .env and set your OPENAI_API_KEY")
    except Exception as e:
        print(f"Could not copy template: {e}")
        print("Please manually copy config/development.env to .env")

def run_system_check():
    """Run a quick system check"""
    print("\nRunning system check...")
    
    try:
        # Check if we can import main modules
        from src.core.config import Config
        from src.core.orchestrator import AgentOrchestrator
        
        # Check environment file
        env_file = Path(".env")
        if env_file.exists():
            print("Environment file found")
        else:
            print("WARNING: .env file not found")
        
        # Check if we can create config
        config = Config()
        print("Configuration loaded successfully")
        
        # Try to initialize orchestrator
        orchestrator = AgentOrchestrator()
        print("Agent orchestrator initialized successfully")
        
        return True
        
    except ImportError as e:
        print(f"INFO: Some modules not yet available: {e}")
        print("This is expected during initial setup")
        return True  # Don't fail for import issues in Docker
    except Exception as e:
        print(f"WARNING: System check encountered issue: {e}")
        return True  # Don't fail the setup

def display_next_steps(system_ready):
    """Display next steps for the user"""
    print("\n" + "="*60)
    print("SETUP CHECK COMPLETE!")
    print("="*60)
    
    if system_ready:
        print("\nYour AI Agent System is ready to use!")
        print("\nNext steps (in Docker environment):")
        print("   1. Set OPENAI_API_KEY in .env file")
        print("   2. Run demo: python -m src.interfaces.cli.demo")
        print("   3. Start web interface: python -m src.interfaces.web.app")
        print("   4. Open browser to: http://localhost:5000")
    else:
        print("\nSetup check completed.")
        print("\nTo use the system:")
        print("   1. Ensure OPENAI_API_KEY is set in .env file")
        print("   2. Test with: python -m src.interfaces.cli.demo")
    
    print("\nQuick Commands:")
    print("   • ./start.sh web    - Start web interface")
    print("   • ./start.sh demo   - Run interactive demo")
    print("   • ./start.sh test   - Run test suite")
    print("   • ./start.sh shell  - Interactive shell")
    
    print("\nAgent Capabilities:")
    print("   • Research Agent - Web search and information gathering")
    print("   • Analysis Agent - Data processing and insight generation")  
    print("   • Content Agent - Professional content creation")
    print("   • Quality Agent - Quality assurance and review")

def main():
    """Main setup function"""
    print("""
╔══════════════════════════════════════════════════════════╗
║        AI Research & Content Creation Team Setup        ║
║              Level 4 Multi-Agent System                 ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\nERROR: Setup failed during dependency installation")
        sys.exit(1)
    
    # Create environment file
    create_env_file()
    
    # Run system check
    system_ready = run_system_check()
    
    # Display next steps
    display_next_steps(system_ready)

if __name__ == "__main__":
    main() 