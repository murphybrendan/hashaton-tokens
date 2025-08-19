// MTG Token Creator - Frontend JavaScript

class TokenCreator {
    constructor() {
        this.selectedCard = null;
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // Search functionality
        document.getElementById('searchBtn').addEventListener('click', () => this.searchCards());
        document.getElementById('cardSearch').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.searchCards();
        });

        // Token generation
        document.getElementById('generateTokenBtn').addEventListener('click', () => this.generateToken());

        // Navigation
        document.getElementById('newTokenBtn').addEventListener('click', () => this.resetToSearch());
        document.getElementById('downloadBtn').addEventListener('click', () => this.downloadToken());
    }

    async searchCards() {
        const query = document.getElementById('cardSearch').value.trim();
        if (!query) {
            this.showError('Please enter a card name to search for.');
            return;
        }

        this.showLoading(true);
        this.hideAllSections();

        try {
            const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
            const data = await response.json();

            if (response.ok && data.cards && data.cards.length > 0) {
                this.displaySearchResults(data.cards);
            } else {
                this.showError('No cards found. Try a different search term.');
            }
        } catch (error) {
            console.error('Search error:', error);
            this.showError('Failed to search for cards. Please try again.');
        } finally {
            this.showLoading(false);
        }
    }

    displaySearchResults(cards) {
        const resultsContainer = document.getElementById('searchResults');
        const resultsList = document.getElementById('resultsList');
        
        resultsList.innerHTML = '';
        
        cards.forEach(card => {
            const cardElement = this.createCardElement(card);
            resultsList.appendChild(cardElement);
        });
        
        resultsContainer.classList.remove('hidden');
    }

    createCardElement(card) {
        const cardDiv = document.createElement('div');
        cardDiv.className = 'result-card';
        cardDiv.addEventListener('click', () => this.selectCard(card));
        
        // Get the best available image
        let imageUrl = '';
        if (card.image_uris && card.image_uris.small) {
            imageUrl = card.image_uris.small;
        } else if (card.card_faces && card.card_faces[0] && card.card_faces[0].image_uris) {
            imageUrl = card.card_faces[0].image_uris.small;
        }

        const manaCost = card.mana_cost || '';
        const typeLine = card.type_line || '';
        
        cardDiv.innerHTML = `
            <img src="${imageUrl}" alt="${card.name}" onerror="this.style.display='none'">
            <div class="result-card-info">
                <h4>${card.name}</h4>
                <p>${manaCost} • ${typeLine}</p>
            </div>
        `;
        
        return cardDiv;
    }

    selectCard(card) {
        this.selectedCard = card;

        // Show customization section
        this.hideAllSections();
        document.getElementById('customizationSection').classList.remove('hidden');
        
        // Scroll to customization section
        document.getElementById('customizationSection').scrollIntoView({ behavior: 'smooth' });
    }

    async generateToken() {
        if (!this.selectedCard) {
            this.showError('Please select a card first.');
            return;
        }

        const tokenData = {
            card_name: this.selectedCard.name,
            power: document.getElementById('power').value.trim(),
            toughness: document.getElementById('toughness').value.trim(),
            subtype: document.getElementById('subtype').value.trim()
        };

        this.showLoading(true);
        this.hideAllSections();

        try {
            const response = await fetch('/api/token/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(tokenData)
            });

            if (response.ok) {
                const blob = await response.blob();
                const imageUrl = URL.createObjectURL(blob);
                
                // Store the blob for download
                this.generatedTokenBlob = blob;
                
                this.displayToken(imageUrl);
            } else {
                const errorData = await response.json();
                this.showError(errorData.error || 'Failed to generate token.');
            }
        } catch (error) {
            console.error('Token generation error:', error);
            this.showError('Failed to generate token. Please try again.');
        } finally {
            this.showLoading(false);
        }
    }

    displayToken(imageUrl) {
        const tokenImage = document.getElementById('tokenImage');
        tokenImage.src = imageUrl;
        
        document.getElementById('previewSection').classList.remove('hidden');
        document.getElementById('previewSection').scrollIntoView({ behavior: 'smooth' });
    }

    downloadToken() {
        if (!this.generatedTokenBlob) {
            this.showError('No token to download.');
            return;
        }

        const url = URL.createObjectURL(this.generatedTokenBlob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `mtg-token-${Date.now()}.png`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    resetToSearch() {
        this.selectedCard = null;
        this.generatedTokenBlob = null;
        
        // Clear form
        document.getElementById('cardSearch').value = '';
        document.getElementById('power').value = '';
        document.getElementById('toughness').value = '';
        document.getElementById('subtype').value = '';
        
        // Uncheck all colors
        document.querySelectorAll('.color-checkbox input').forEach(checkbox => {
            checkbox.checked = false;
        });
        
        // Show search section
        this.hideAllSections();
        document.getElementById('searchResults').classList.add('hidden');
    }

    hideAllSections() {
        document.getElementById('searchResults').classList.add('hidden');
        document.getElementById('customizationSection').classList.add('hidden');
        document.getElementById('previewSection').classList.add('hidden');
    }

    showLoading(show) {
        const loading = document.getElementById('loading');
        if (show) {
            loading.classList.remove('hidden');
        } else {
            loading.classList.add('hidden');
        }
    }

    showError(message) {
        // Create a simple error notification
        const errorDiv = document.createElement('div');
        errorDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #dc3545;
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            z-index: 1000;
            max-width: 300px;
            font-weight: 500;
        `;
        errorDiv.textContent = message;
        
        document.body.appendChild(errorDiv);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.parentNode.removeChild(errorDiv);
            }
        }, 5000);
    }
}

// Initialize the application when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new TokenCreator();
});
