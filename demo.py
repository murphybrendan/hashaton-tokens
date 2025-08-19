#!/usr/bin/env python3
"""
Demo script for MTG Token Creator
This script demonstrates how to use the token creation functionality programmatically
"""

import requests
import json
import time

def demo_token_creation():
    """Demonstrate the token creation process"""
    print("🃏 MTG Token Creator Demo")
    print("=" * 50)
    
    # Base URL for the local server
    base_url = "http://localhost:5000"
    
    # Step 1: Search for a card
    print("\n1. 🔍 Searching for 'Esper Sentinel'...")
    search_response = requests.get(f"{base_url}/api/search?q=Esper+Sentinel")
    
    if search_response.status_code != 200:
        print("❌ Failed to search for cards")
        return
    
    search_data = search_response.json()
    if not search_data.get('cards'):
        print("❌ No cards found")
        return
    
    card = search_data['cards'][0]
    print(f"✅ Found: {card['name']}")
    print(f"   Mana Cost: {card.get('mana_cost', 'N/A')}")
    print(f"   Type: {card.get('type_line', 'N/A')}")
    print(f"   Colors: {card.get('colors', [])}")
    
    # Step 2: Generate a token
    print("\n2. 🎨 Generating token...")
    token_data = {
        "card_name": card['name'],
        "token_name": "Esper Sentinel Token",
        "token_type": "Creature",
        "power": "2",
        "toughness": "2",
        "colors": ["White"]
    }
    
    generate_response = requests.post(
        f"{base_url}/api/token/generate",
        json=token_data,
        headers={'Content-Type': 'application/json'}
    )
    
    if generate_response.status_code == 200:
        print("✅ Token generated successfully!")
        print(f"   Token size: {len(generate_response.content)} bytes")
        print(f"   Content type: {generate_response.headers.get('content-type', 'N/A')}")
        
        # Save the token
        filename = f"demo_token_{int(time.time())}.png"
        with open(filename, 'wb') as f:
            f.write(generate_response.content)
        print(f"   Token saved as: {filename}")
        
    else:
        print(f"❌ Failed to generate token: {generate_response.status_code}")
        try:
            error_data = generate_response.json()
            print(f"   Error: {error_data.get('error', 'Unknown error')}")
        except:
            print(f"   Response: {generate_response.text}")
    
    # Step 3: Test with different card
    print("\n3. 🔍 Searching for 'Lightning Bolt'...")
    search_response = requests.get(f"{base_url}/api/search?q=Lightning+Bolt")
    
    if search_response.status_code == 200:
        search_data = search_response.json()
        if search_data.get('cards'):
            card = search_data['cards'][0]
            print(f"✅ Found: {card['name']}")
            print(f"   Mana Cost: {card.get('mana_cost', 'N/A')}")
            print(f"   Type: {card.get('type_line', 'N/A')}")
            print(f"   Colors: {card.get('colors', [])}")
            
            # Generate a different type of token
            print("\n4. 🎨 Generating Lightning Bolt token...")
            token_data = {
                "card_name": card['name'],
                "token_name": "Lightning Bolt Token",
                "token_type": "Instant",
                "power": "",
                "toughness": "",
                "colors": ["Red"]
            }
            
            generate_response = requests.post(
                f"{base_url}/api/token/generate",
                json=token_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if generate_response.status_code == 200:
                print("✅ Lightning Bolt token generated successfully!")
                filename = f"lightning_bolt_token_{int(time.time())}.png"
                with open(filename, 'wb') as f:
                    f.write(generate_response.content)
                print(f"   Token saved as: {filename}")
            else:
                print(f"❌ Failed to generate Lightning Bolt token")
        else:
            print("❌ No Lightning Bolt cards found")
    else:
        print("❌ Failed to search for Lightning Bolt")
    
    print("\n" + "=" * 50)
    print("🎉 Demo completed!")
    print("💡 Check the generated PNG files in the current directory")
    print("🌐 Open http://localhost:5000 in your browser for the web interface")

if __name__ == '__main__':
    try:
        demo_token_creation()
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to the server. Make sure it's running with:")
        print("   source venv/bin/activate && python3 run.py")
    except Exception as e:
        print(f"❌ Demo failed with error: {e}")
