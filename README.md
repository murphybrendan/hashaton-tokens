# MTG Token Creator 🃏

A web-based tool for creating custom Magic: The Gathering tokens using Scryfall's API. This application allows you to search for MTG cards, retrieve their art, and generate custom token cards with personalized names, types, power/toughness, and colors.

## Features

- **Card Search**: Search for MTG cards using Scryfall's comprehensive database
- **Art Retrieval**: Automatically fetch high-quality card art in art_crop format
- **Professional Frame Template**: Uses custom black frame template for authentic MTG look
- **Token Customization**: 
  - Custom token names
  - Token types (Creature, Artifact, Enchantment, Land, Planeswalker)
  - Meta types (e.g., Zombie, Soldier, Goblin) for detailed creature classification
  - Power and toughness values
  - Color selection (White, Blue, Black, Red, Green)
- **Auto-color Detection**: Automatically detects card colors from mana cost
- **Artist Attribution**: Automatically includes artist credit from the original card
- **High-Quality Output**: Generates PNG tokens using the frame template
- **Responsive Design**: Works on desktop and mobile devices
- **Download Support**: Save your generated tokens locally

## How It Works

1. **Search**: Enter a card name (e.g., "Esper Sentinel") to search Scryfall's database
2. **Select**: Choose from search results to select your base card
3. **Customize**: Modify token properties like name, type, power/toughness, and colors
4. **Generate**: Create your custom token using the selected card's art
5. **Download**: Save your token as a PNG file

## API Endpoints

- `GET /api/search?q=<query>` - Search for cards
- `GET /api/card/<card_id>` - Get detailed card information
- `POST /api/token/generate` - Generate a custom token

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd hashaton-tokens
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

## Usage Examples

### Basic Token Creation

1. Search for "Esper Sentinel"
2. Select the card from search results
3. Customize your token:
   - Name: "Esper Sentinel Token"
   - Type: Creature
   - Power: 2
   - Toughness: 2
   - Colors: White (auto-detected)
4. Click "Generate Token"
5. Download your custom token

### Advanced Customization

- **Token Types**: Choose from various card types
- **Color Combinations**: Select multiple colors for hybrid tokens
- **Power/Toughness**: Add combat stats for creature tokens
- **Custom Names**: Create unique token identities

## Technical Details

### Backend (Flask)
- **Framework**: Flask with CORS support
- **Image Processing**: Pillow (PIL) for token generation
- **API Integration**: Scryfall REST API
- **Image Format**: PNG with transparency support

### Frontend
- **Framework**: Vanilla JavaScript (ES6+)
- **Styling**: Modern CSS with responsive design
- **UI Components**: Custom-built interface components
- **Error Handling**: User-friendly error notifications

### Image Processing
- **Input**: Scryfall art_crop images
- **Output**: 421x614 PNG tokens (standard MTG dimensions)
- **Features**: 
  - High-quality image resizing
  - Text overlay with readability
  - Color-accurate rendering
  - Transparent backgrounds

## Dependencies

- **Flask**: Web framework
- **requests**: HTTP library for API calls
- **Pillow**: Image processing library
- **python-dotenv**: Environment variable management
- **flask-cors**: Cross-origin resource sharing

## Browser Compatibility

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Acknowledgments

- **Scryfall**: For providing the comprehensive MTG card database and API
- **Wizards of the Coast**: For Magic: The Gathering
- **Open Source Community**: For the amazing tools and libraries used

## Support

If you encounter any issues or have questions:

1. Check the browser console for error messages
2. Verify your internet connection (required for Scryfall API)
3. Ensure all dependencies are properly installed
4. Check that the Flask server is running

## Future Enhancements

- [ ] Multiple token templates
- [ ] Batch token generation
- [ ] Advanced text formatting
- [ ] Token border customization
- [ ] Export to different formats
- [ ] Token gallery and sharing
- [ ] Advanced search filters
- [ ] Token statistics tracking
