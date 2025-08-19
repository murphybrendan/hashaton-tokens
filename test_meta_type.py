#!/usr/bin/env python3
"""
Test script for meta type functionality
Tests the new meta type feature with the black frame template
"""

import requests
import json
import time

def test_meta_type():
    """Test the meta type functionality"""
    print("🧪 Testing Meta Type Functionality")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    # Test 1: Creature with meta type
    print("\n1. 🎨 Testing Creature with Meta Type...")
    token_data = {
        "card_name": "Esper Sentinel",
        "token_name": "Zombie Token",
        "token_type": "Creature",
        "power": "2",
        "toughness": "2",
        "colors": ["Black"],
        "meta_type": "Zombie"
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/token/generate",
            json=token_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            filename = f"zombie_token_{int(time.time())}.png"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"✅ Zombie token generated successfully!")
            print(f"   File: {filename}")
            print(f"   Size: {len(response.content)} bytes")
            print(f"   Expected type: Creature - Zombie - Black")
        else:
            print(f"❌ Failed to generate zombie token: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error generating zombie token: {e}")
    
    # Test 2: Creature with different meta type
    print("\n2. 🎨 Testing Creature with Different Meta Type...")
    token_data = {
        "card_name": "Lightning Bolt",
        "token_name": "Goblin Token",
        "token_type": "Creature",
        "power": "1",
        "toughness": "1",
        "colors": ["Red"],
        "meta_type": "Goblin"
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/token/generate",
            json=token_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            filename = f"goblin_token_{int(time.time())}.png"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"✅ Goblin token generated successfully!")
            print(f"   File: {filename}")
            print(f"   Size: {len(response.content)} bytes")
            print(f"   Expected type: Creature - Goblin - Red")
        else:
            print(f"❌ Failed to generate goblin token: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error generating goblin token: {e}")
    
    # Test 3: Non-creature with meta type
    print("\n3. 🎨 Testing Non-Creature with Meta Type...")
    token_data = {
        "card_name": "Esper Sentinel",
        "token_name": "Treasure Token",
        "token_type": "Artifact",
        "power": "",
        "toughness": "",
        "colors": [],
        "meta_type": "Treasure"
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/token/generate",
            json=token_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            filename = f"treasure_token_{int(time.time())}.png"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"✅ Treasure token generated successfully!")
            print(f"   File: {filename}")
            print(f"   Size: {len(response.content)} bytes")
            print(f"   Expected type: Artifact - Treasure")
        else:
            print(f"❌ Failed to generate treasure token: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error generating treasure token: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Meta type testing completed!")
    print("💡 Check the generated PNG files to verify the frame template and text placement")

if __name__ == '__main__':
    try:
        test_meta_type()
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to the server. Make sure it's running with:")
        print("   source venv/bin/activate && python3 run.py")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
