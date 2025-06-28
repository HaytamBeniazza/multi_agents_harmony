#!/usr/bin/env python3
"""
Simple test to verify the web interface is working
"""

import requests
import time

def test_web_interface():
    base_url = "http://127.0.0.1:5000"
    
    print("🧪 Testing AI Research Web Interface...")
    
    # Test 1: Check if the main page loads
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200 and "AI Research" in response.text:
            print("✅ Main page loads successfully")
        else:
            print("❌ Main page failed to load")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to web interface: {e}")
        print("   Make sure the web interface is running")
        return False
    
    print("\n🎯 Web Interface Test Complete!")
    print(f"   Access your web interface at: {base_url}")
    
    return True

if __name__ == "__main__":
    test_web_interface() 