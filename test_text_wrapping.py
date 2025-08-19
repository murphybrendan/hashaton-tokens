#!/usr/bin/env python3
"""
Test script for text wrapping functionality
Tests the new text wrapping feature with the black frame template
"""

import requests
import json
import time

def test_text_wrapping():
    """Test the text wrapping functionality"""
    print("🧪 Testing Text Wrapping Functionality")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    # Test 1: Card with short oracle text
    print("\n1. 🎨 Testing Short Oracle Text...")
    token_data = {
        "card_name": "Esper Sentinel",
        "power": "2",
        "toughness": "2",
        "subtype": "Zombie"
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/token/generate",
            json=token_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            filename = f"short_text_token_{int(time.time())}.png"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"✅ Short text token generated successfully!")
            print(f"   File: {filename}")
            print(f"   Size: {len(response.content)} bytes")
        else:
            print(f"❌ Failed to generate short text token: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error generating short text token: {e}")
    
    # Test 2: Card with long oracle text (should test wrapping)
    print("\n2. 🎨 Testing Long Oracle Text (Wrapping)...")
    token_data = {
        "card_name": "Lightning Bolt",
        "power": "",
        "toughness": "",
        "subtype": "Instant"
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/token/generate",
            json=token_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            filename = f"long_text_token_{int(time.time())}.png"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"✅ Long text token generated successfully!")
            print(f"   File: {filename}")
            print(f"   Size: {len(response.content)} bytes")
            print(f"   This should test the text wrapping functionality")
        else:
            print(f"❌ Failed to generate long text token: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error generating long text token: {e}")
    
    # Test 3: Card with very long oracle text
    print("\n3. 🎨 Testing Very Long Oracle Text (Multiple Lines)...")
    token_data = {
        "card_name": "Esper Sentinel",
        "power": "3",
        "toughness": "3",
        "subtype": "Soldier"
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/token/generate",
            json=token_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            filename = f"very_long_text_token_{int(time.time())}.png"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"✅ Very long text token generated successfully!")
            print(f"   File: {filename}")
            print(f"   Size: {len(response.content)} bytes")
            print(f"   This should test multiple line wrapping")
        else:
            print(f"❌ Failed to generate very long text token: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error generating very long text token: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Text wrapping testing completed!")
    print("💡 Check the generated PNG files to verify:")
    print("   - Text is properly wrapped within the rules box")
    print("   - No text extends outside the boundaries")
    print("   - Multiple lines are properly spaced")
    print("   - Font sizes are appropriate for readability")

if __name__ == '__main__':
    try:
        test_text_wrapping()
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to the server. Make sure it's running with:")
        print("   source venv/bin/activate && python3 run.py")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
