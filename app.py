from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
import requests
import io
from PIL import Image, ImageDraw, ImageFont
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = Flask(__name__)
CORS(app)

# Scryfall API base URL
SCRYFALL_BASE_URL = "https://api.scryfall.com"


# Load the fonts
current_dir = os.path.dirname(os.path.abspath(__file__))
fonts_dir = os.path.join(current_dir, 'static', 'fonts')
title_font = ImageFont.truetype(os.path.join(fonts_dir, "Beleren2016-Bold.ttf"), 100)
type_font = ImageFont.truetype(os.path.join(fonts_dir, "Beleren2016-Bold.ttf"), 80)
artist_font = ImageFont.truetype(os.path.join(fonts_dir, "Beleren2016SmallCaps-Bold.ttf"), 50)
pt_font = ImageFont.truetype(os.path.join(fonts_dir, "Beleren2016-Bold.ttf"), 100)
oracle_font = ImageFont.truetype(os.path.join(fonts_dir, "MPlantin-Regular.ttf"), 80)
frame_path = os.path.join(os.path.dirname(__file__), 'static', 'images', 'black-frame.png')
frame = Image.open(frame_path).convert('RGBA')


@app.route('/')
def index():
    """Main page for the token creator"""
    return render_template('index.html')

@app.route('/api/search', methods=['GET'])
def search_cards():
    """Search for cards using Scryfall API"""
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': 'Query parameter required'}), 400
    
    try:
        # Search for cards
        search_url = f"{SCRYFALL_BASE_URL}/cards/search"
        params = {'q': query}
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        if data.get('data'):
            # Return first few results
            cards = data['data'][:5]  # Limit to 5 results
            return jsonify({
                'cards': cards,
                'total': data.get('total_cards', 0)
            })
        else:
            return jsonify({'cards': [], 'total': 0})
            
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'API request failed: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

@app.route('/api/card/<card_id>')
def get_card_details(card_id):
    """Get detailed information about a specific card"""
    try:
        response = requests.get(f"{SCRYFALL_BASE_URL}/cards/{card_id}")
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Failed to fetch card: {str(e)}'}), 500

@app.route('/api/token/generate', methods=['POST'])
def generate_token():
    """Generate a token using card art and custom parameters"""
    try:
        data = request.json
        card_name = data.get('card_name')
        power = data.get('power', '')
        toughness = data.get('toughness', '')
        subtype = data.get('subtype', '')
        
        if not card_name:
            return jsonify({'error': 'Card name is required'}), 400
        
        # Search for the card
        search_url = f"{SCRYFALL_BASE_URL}/cards/search"
        params = {'q': f'name:"{card_name}"'}
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        
        search_data = response.json()
        if not search_data.get('data'):
            return jsonify({'error': 'Card not found'}), 404
        
        card = search_data['data'][0]

        # Get the types
        if 'type_line' in card:
            type_line = card['type_line']
            if '—' in type_line:
                meta_types, subtypes = type_line.split('—', 1)
                meta_types = meta_types.strip()
                subtypes = subtypes.strip()
            else:
                # No separator, treat the whole thing as meta types
                meta_types = type_line.strip()
                subtypes = ""
            
            # Ensure meta_types ends with 'Creature' if it's a creature type
            if 'Creature' in meta_types and not meta_types.endswith('Creature'):
                meta_types += ' Creature'
        else:
            meta_types = "Creature"
            subtypes = ""

        if "oracle_text" in card:
            oracle_text = card['oracle_text']
        else:
            oracle_text = ""
        
        if "mana_cost" in card:
            mana_cost = card['mana_cost']
        else:
            mana_cost = ""
        
        # Get the art crop image
        if 'image_uris' in card and 'art_crop' in card['image_uris']:
            art_url = card['image_uris']['art_crop']
        else:
            # For double-faced cards, try to get the first face
            if 'card_faces' in card and card['card_faces']:
                art_url = card['card_faces'][0].get('image_uris', {}).get('art_crop')
            else:
                return jsonify({'error': 'No art available for this card'}), 404
        
        if not art_url:
            return jsonify({'error': 'No art available for this card'}), 404
        
        
        # Download the art
        art_response = requests.get(art_url)
        art_response.raise_for_status()
        
        # Create the token
        artist_name = card.get('artist', '')
        token_image = create_token(
            art_response.content,
            card['name'],
            power,
            toughness,
            meta_types,
            subtype,
            oracle_text,
            mana_cost,
            artist_name
        )
        
        # Return the token image
        img_io = io.BytesIO()
        token_image.save(img_io, 'PNG')
        img_io.seek(0)
        
        return send_file(img_io, mimetype='image/png')
        
    except Exception as e:
        return jsonify({'error': f'Failed to generate token: {str(e)}'}), 500

def wrap_text(text, font, max_width):
    """Wrap text to fit within a specified width, breaking at word boundaries"""
    if not text:
        return []
    
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        # Test if adding this word would exceed the width
        test_line = ' '.join(current_line + [word])
        bbox = font.getbbox(test_line)
        line_width = bbox[2] - bbox[0]
        
        if line_width <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                # Single word is too long, force break it
                lines.append(word)
    
    # Add the last line
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines

def create_token(art_data, token_name, power, toughness, meta_types, subtype, oracle_text, mana_cost, artist_name=""):
    """Create a token image using the black frame template"""
    # Load the art
    art_image = Image.open(io.BytesIO(art_data))
    
    # Get frame dimensions
    frame_width, frame_height = frame.size
    
    # Resize art to fit the transparent area (approximate dimensions for the art box)
    # These coordinates are estimates - you may need to adjust based on your actual frame
    art_box_width = int(frame_width * 0.85)  # Art box is roughly 85% of frame width
    art_box_height = int(frame_height * 0.45)  # Art box is roughly 45% of frame height
    art_box_x = int(frame_width * 0.075)      # Art box starts at roughly 7.5% from left
    art_box_y = int(frame_height * 0.11)     # Art box starts at roughly 10% from top
    
    # Resize art to fit the art box while maintaining aspect ratio
    art_image = art_image.resize((art_box_width, art_box_height), Image.Resampling.LANCZOS)
    
    # Create a new image with the frame dimensions
    token = Image.new('RGBA', (frame_width, frame_height), (0, 0, 0, 0))
    
    # Paste the art in the center of the art box
    art_x = art_box_x + (art_box_width - art_image.width) // 2
    art_y = art_box_y + (art_box_height - art_image.height) // 2
    token.paste(art_image, (art_x, art_y))

    # Overlay the frame
    token.paste(frame, (0, 0), frame)
    
    # Add text elements
    draw = ImageDraw.Draw(token)
    
    # Add token name in the top title box (approximate coordinates)
    text_x = int(frame_width * 0.09)
    title_y = int(frame_height * 0.06)  # Roughly 8% from top
    
    # Center the title text horizontally across the entire frame
    draw.text((text_x, title_y), token_name, fill=(0, 0, 0), font=title_font)

    # Add mana cost
    mana_cost_y = title_y
    mana_cost_x = int(frame_width * 0.91)
    draw.text((mana_cost_x, mana_cost_y), mana_cost, fill=(0, 0, 0), font=title_font, anchor='ra')
    
    # Add token type below the art (approximate coordinates)
    type_y = int(frame_height * 0.575)  # Roughly 50% from top
    
    # Build type text with meta types
    type_text = f"{meta_types} - {subtype}"
    draw.text((text_x, type_y), type_text, fill=(0, 0, 0), font=type_font)

    # Add oracle text below the type text (approximate coordinates)
    oracle_y = int(frame_height * 0.65)  # Roughly 65% from top
    
    # Calculate the width of the rules text box (approximate)
    rules_box_width = int(frame_width - 2*text_x)
    
    # Wrap the oracle text to fit within the rules box
    wrapped_lines = wrap_text(oracle_text, oracle_font, rules_box_width)
    
    # Draw each wrapped line
    line_height = oracle_font.getbbox("Ay")[3]  # Get approximate line height
    for i, line in enumerate(wrapped_lines):
        line_y = oracle_y + (i * line_height)
        draw.text((text_x, line_y), line, fill=(0, 0, 0), font=oracle_font)
    
    # Add power/toughness if provided (approximate coordinates)
    if power and toughness:
        pt_text = f"{power}/{toughness}"
        pt_x = int(frame_width * 0.86)  # Roughly 80% from left
        pt_y = int(frame_height * 0.92)  # Roughly 80% from top
        
        # Center the power/toughness text
        draw.text((pt_x, pt_y), pt_text, fill=(0, 0, 0), font=pt_font, anchor='mm')
    
    # Add artist attribution at the bottom (approximate coordinates)
    if artist_name:
        artist_y = int(frame_height * 0.955)  # Roughly 95% from top
        artist_x = int(frame_width * 0.195)  # Roughly 20% from left
        
        # Center the artist text
        draw.text((artist_x, artist_y), artist_name, fill=(255, 255, 255), font=artist_font)
    
    return token

def create_basic_token(art_data, token_name, power, toughness, token_type, colors, meta_type=""):
    """Fallback token creation method if frame template fails"""
    # Load the art
    art_image = Image.open(io.BytesIO(art_data))
    
    # Create a new image with token dimensions (standard MTG card size)
    token_width = 421
    token_height = 614
    
    # Create the token base
    token = Image.new('RGBA', (token_width, token_height), (0, 0, 0, 0))
    
    # Resize and paste the art
    art_image = art_image.resize((token_width, token_height), Image.Resampling.LANCZOS)
    token.paste(art_image, (0, 0))
    
    # Add a semi-transparent overlay for text readability
    overlay = Image.new('RGBA', (token_width, token_height), (0, 0, 0, 100))
    token = Image.alpha_composite(token, overlay)
    
    # Add text elements
    draw = ImageDraw.Draw(token)
    
    # Try to load a font, fall back to default if not available
    try:
        title_font = ImageFont.truetype("arial.ttf", 24)
        stats_font = ImageFont.truetype("arial.ttf", 20)
    except:
        title_font = ImageFont.load_default()
        stats_font = ImageFont.load_default()
    
    # Add token name at the top
    text_bbox = draw.textbbox((0, 0), token_name, font=title_font)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = (token_width - text_width) // 2
    draw.text((text_x, 20), token_name, fill=(255, 255, 255), font=title_font)
    
    # Add token type
    type_text = token_type
    if meta_type:
        type_text += f" - {meta_type}"
    if colors:
        type_text += f" - {' '.join(colors)}"
    
    text_bbox = draw.textbbox((0, 0), type_text, font=stats_font)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = (token_width - text_width) // 2
    draw.text((text_x, 50), type_text, fill=(255, 255, 255), font=stats_font)
    
    # Add power/toughness if provided
    if power and toughness:
        pt_text = f"{power}/{toughness}"
        text_bbox = draw.textbbox((0, 0), pt_text, font=stats_font)
        text_width = text_bbox[2] - text_bbox[0]
        text_x = (token_width - text_width) // 2
        draw.text((text_x, token_height - 40), pt_text, fill=(255, 255, 255), font=stats_font)
    
    return token

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
