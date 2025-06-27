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
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version {sys.version_info.major}.{sys.version_info.minor} is compatible")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    try:
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True, capture_output=True, text=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        print(f"Error output: {e.stderr}")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path(".env")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return
    
    print("\n📝 Creating .env file...")
    
    # Get OpenAI API key from user
    api_key = input("Enter your OpenAI API key (or press Enter to set later): ").strip()
    
    env_content = f"""# AI Research & Content Creation Team Configuration

# OpenAI Configuration
OPENAI_API_KEY={api_key}
OPENAI_MODEL=gpt-4-turbo-preview
OPENAI_TEMPERATURE=0.7

# Web Scraping Configuration
USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36
REQUEST_TIMEOUT=30
MAX_RETRIES=3

# Agent Configuration
MAX_RESEARCH_SOURCES=5
MIN_CONTENT_LENGTH=1000
QUALITY_THRESHOLD=0.8

# Web Interface Configuration
FLASK_HOST=localhost
FLASK_PORT=5000
FLASK_DEBUG=True

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=agent_system.log
"""
    
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print("✅ .env file created")
    
    if not api_key:
        print("⚠️  Don't forget to add your OpenAI API key to the .env file!")

def run_system_check():
    """Run a quick system check"""
    print("\n🔍 Running system check...")
    
    try:
        # Import main modules to check for issues
        from config import config
        from orchestrator import AgentOrchestrator
        
        # Validate configuration
        config_status = config.validate_config()
        
        if config_status['valid']:
            print("✅ System configuration is valid")
        else:
            print("⚠️  Configuration issues found:")
            for issue in config_status['issues']:
                print(f"   • {issue}")
        
        # Try to initialize orchestrator
        orchestrator = AgentOrchestrator()
        print("✅ Agent orchestrator initialized successfully")
        
        return config_status['valid']
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ System check failed: {e}")
        return False

def display_next_steps(system_ready):
    """Display next steps for the user"""
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETE!")
    print("="*60)
    
    if system_ready:
        print("\n✅ Your AI Agent System is ready to use!")
        print("\n🚀 Next steps:")
        print("   1. Run the demo: python demo.py")
        print("   2. Start web interface: python web_interface.py")
        print("   3. Open browser to: http://localhost:5000")
    else:
        print("\n⚠️  Setup completed with some issues.")
        print("\n🔧 To fix issues:")
        print("   1. Add your OpenAI API key to .env file")
        print("   2. Check all dependencies are installed")
        print("   3. Run: python demo.py to test")
    
    print("\n📚 Documentation:")
    print("   • README.md - Complete project documentation")  
    print("   • demo.py - Interactive demonstration")
    print("   • web_interface.py - Web interface")
    
    print("\n🤖 Agent Capabilities:")
    print("   • 🔍 Research Agent - Web search and information gathering")
    print("   • 📊 Analysis Agent - Data processing and insight generation")
    print("   • 📝 Content Agent - Professional content creation")
    print("   • ✅ Quality Agent - Quality assurance and review")

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
        print("\n❌ Setup failed during dependency installation")
        sys.exit(1)
    
    # Create environment file
    create_env_file()
    
    # Run system check
    system_ready = run_system_check()
    
    # Display next steps
    display_next_steps(system_ready)

if __name__ == "__main__":
    main() 