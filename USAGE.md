# MTG Token Creator - Usage Guide

## Quick Start

### 1. Start the Server
```bash
# Activate virtual environment
source venv/bin/activate

# Start the server
python3 run.py
```

### 2. Open Your Browser
Navigate to: `http://localhost:5000`

### 3. Create Your First Token
1. Search for a card (e.g., "Esper Sentinel")
2. Select the card from results
3. Customize your token
4. Click "Generate Token"
5. Download your custom token

## Web Interface Features

### Search Section
- **Card Search**: Enter any MTG card name
- **Real-time Results**: See up to 5 matching cards
- **Card Preview**: View card image, mana cost, and type
- **Smart Selection**: Click any result to select it

### Customization Section
- **Token Name**: Customize the token's name
- **Token Type**: Choose from Creature, Artifact, Enchantment, Land, or Planeswalker
- **Meta Type**: Add specific creature types (e.g., Zombie, Soldier, Goblin)
- **Power/Toughness**: Add combat stats for creature tokens
- **Colors**: Select one or more colors (auto-detected from original card)
- **Auto-fill**: Token name and colors are automatically populated
- **Artist Credit**: Automatically included from the original card

### Preview & Download
- **Live Preview**: See your token before downloading
- **High Quality**: PNG format at standard MTG dimensions (421x614)
- **Instant Download**: Save tokens directly to your device
- **Create More**: Generate additional tokens easily

## API Usage

### Search for Cards
```bash
GET /api/search?q=<card_name>

# Example
curl "http://localhost:5000/api/search?q=Esper+Sentinel"
```

### Generate Token
```bash
POST /api/token/generate
Content-Type: application/json

{
  "card_name": "Esper Sentinel",
  "token_name": "Custom Token",
  "token_type": "Creature",
  "power": "2",
  "toughness": "2",
  "colors": ["White"]
}
```

### Get Card Details
```bash
GET /api/card/<card_id>

# Example
curl "http://localhost:5000/api/card/f3537b5b-5c6b-4c6b-8c6b-4c6b8c6b4c6b"
```

## Programmatic Usage

### Python Example
```python
import requests

# Search for a card
response = requests.get("http://localhost:5000/api/search?q=Esper+Sentinel")
cards = response.json()['cards']

# Generate a token
token_data = {
    "card_name": cards[0]['name'],
    "token_name": "My Custom Token",
    "token_type": "Creature",
    "power": "3",
    "toughness": "3",
    "colors": ["White", "Blue"]
}

response = requests.post(
    "http://localhost:5000/api/token/generate",
    json=token_data
)

# Save the token
with open("my_token.png", "wb") as f:
    f.write(response.content)
```

### Demo Script
Run the included demo script to see examples:
```bash
source venv/bin/activate
python3 demo.py
```

## Token Customization Options

### Token Types
- **Creature**: Add power/toughness, perfect for combat tokens
- **Artifact**: Great for equipment or artifact tokens
- **Enchantment**: Ideal for aura or enchantment tokens
- **Land**: Perfect for land tokens
- **Planeswalker**: For planeswalker tokens

### Color Selection
- **White (W)**: ⚪
- **Blue (U)**: 🔵
- **Black (B)**: ⚫
- **Red (R)**: 🔴
- **Green (G)**: 🟢

### Power/Toughness
- **Format**: Single numbers (e.g., "2", "5", "*")
- **Special Values**: Use "*" for variable power/toughness
- **Empty**: Leave blank for non-creature tokens

## Advanced Features

### Auto-Color Detection
The tool automatically detects card colors from mana cost:
- `{W}` → White
- `{U}` → Blue
- `{B}` → Black
- `{R}` → Red
- `{G}` → Green
- `{1}` → Colorless

### Image Quality
- **Input**: Scryfall art_crop images (high quality)
- **Output**: 421x614 PNG (standard MTG card size)
- **Format**: PNG with transparency support
- **Optimization**: High-quality resizing and text rendering

### Error Handling
- **User-friendly messages**: Clear error descriptions
- **Graceful fallbacks**: Handles missing images gracefully
- **API validation**: Proper input validation and sanitization

## Troubleshooting

### Common Issues

#### Server Won't Start
```bash
# Check if port 5000 is in use
lsof -i :5000

# Kill process if needed
kill -9 <PID>

# Or use different port in app.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

#### Dependencies Missing
```bash
# Reinstall dependencies
source venv/bin/activate
pip install -r requirements.txt
```

#### API Errors
- Check internet connection (required for Scryfall)
- Verify server is running
- Check browser console for errors
- Ensure proper JSON format for POST requests

#### Image Generation Fails
- Verify card name is correct
- Check if card has available art
- Ensure all required fields are filled
- Check server logs for detailed errors

### Performance Tips

#### For Large Numbers of Tokens
- Use the API directly for batch processing
- Implement rate limiting if needed
- Cache frequently used card data
- Consider using async requests for multiple tokens

#### Image Optimization
- Tokens are generated at optimal size
- PNG format provides best quality
- Transparent backgrounds for easy integration
- Standard dimensions for printing

## Examples

### Creature Token with Meta Type
```json
{
  "card_name": "Esper Sentinel",
  "token_name": "Zombie Token",
  "token_type": "Creature",
  "power": "2",
  "toughness": "2",
  "colors": ["Black"],
  "meta_type": "Zombie"
}
```

### Artifact Token
```json
{
  "card_name": "Sol Ring",
  "token_name": "Treasure Token",
  "token_type": "Artifact",
  "power": "",
  "toughness": "",
  "colors": []
}
```

### Multi-Color Token
```json
{
  "card_name": "Lightning Helix",
  "token_name": "Boros Token",
  "token_type": "Creature",
  "power": "3",
  "toughness": "3",
  "colors": ["White", "Red"]
}
```

## Support & Contributing

### Getting Help
1. Check the browser console for errors
2. Verify all dependencies are installed
3. Test the API endpoints directly
4. Check the server logs

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Feature Requests
- Multiple token templates
- Advanced text formatting
- Token border customization
- Batch token generation
- Export to different formats

## License
This project is open source and available under the MIT License.
