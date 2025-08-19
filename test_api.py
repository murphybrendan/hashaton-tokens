#!/usr/bin/env python3
"""
Test script for Scryfall API integration
Run this to verify the API is working before starting the main application
"""

import requests
import json

def test_scryfall_api():
    """Test basic Scryfall API functionality"""
    print("🧪 Testing Scryfall API integration...")
    print("-" * 50)
    
    # Test 1: Basic search
    print("1. Testing card search...")
    try:
        response = requests.get("https://api.scryfall.com/cards/search?q=Esper+Sentinel")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Search successful! Found {data.get('total_cards', 0)} cards")
            
            if data.get('data'):
                first_card = data['data'][0]
                print(f"   First result: {first_card.get('name', 'Unknown')}")
                print(f"   Mana cost: {first_card.get('mana_cost', 'N/A')}")
                print(f"   Type: {first_card.get('type_line', 'N/A')}")
                
                # Test 2: Image URLs
                if 'image_uris' in first_card:
                    print(f"   Art crop available: {'art_crop' in first_card['image_uris']}")
                    if 'art_crop' in first_card['image_uris']:
                        print(f"   Art crop URL: {first_card['image_uris']['art_crop'][:50]}...")
                else:
                    print("   ⚠️  No image_uris found (might be double-faced card)")
                    
            else:
                print("❌ No cards found in search results")
                
        else:
            print(f"❌ Search failed with status code: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Search test failed: {e}")
        return False
    
    # Test 3: Direct card lookup
    print("\n2. Testing direct card lookup...")
    try:
        response = requests.get("https://api.scryfall.com/cards/named?fuzzy=Esper+Sentinel")
        if response.status_code == 200:
            card = response.json()
            print(f"✅ Direct lookup successful!")
            print(f"   Card: {card.get('name', 'Unknown')}")
            print(f"   Set: {card.get('set_name', 'N/A')}")
            print(f"   Rarity: {card.get('rarity', 'N/A')}")
        else:
            print(f"❌ Direct lookup failed with status code: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Direct lookup test failed: {e}")
        return False
    
    # Test 4: Image download test
    print("\n3. Testing image download...")
    try:
        response = requests.get("https://api.scryfall.com/cards/search?q=Esper+Sentinel")
        if response.status_code == 200:
            data = response.json()
            if data.get('data') and 'image_uris' in data['data'][0]:
                art_url = data['data'][0]['image_uris'].get('art_crop')
                if art_url:
                    img_response = requests.get(art_url)
                    if img_response.status_code == 200:
                        print(f"✅ Image download successful!")
                        print(f"   Image size: {len(img_response.content)} bytes")
                        print(f"   Content type: {img_response.headers.get('content-type', 'N/A')}")
                    else:
                        print(f"❌ Image download failed with status code: {img_response.status_code}")
                else:
                    print("⚠️  No art_crop URL available for testing")
            else:
                print("⚠️  No image data available for testing")
        else:
            print("❌ Cannot test image download - search failed")
            
    except Exception as e:
        print(f"❌ Image download test failed: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All tests completed!")
    print("💡 If all tests passed, you're ready to run the main application!")
    print("🚀 Run: python run.py")
    
    return True

if __name__ == '__main__':
    test_scryfall_api()
