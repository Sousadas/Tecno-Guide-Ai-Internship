import os
import requests
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_folder='static')

GEMINI_API_KEY = os.getenv('GOOGLE_GEMINI')
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(app.static_folder, path)

@app.route('/api/chat', methods=['POST'])
def chat():
    if not GEMINI_API_KEY or GEMINI_API_KEY == 'your_api_key_here':
        return jsonify({'error': 'Gemini API key is missing or invalid in the backend.'}), 500

    data = request.json
    user_message = data.get('message')

    if not user_message:
        return jsonify({'error': 'Message is required.'}), 400

    # Prepare payload for Gemini API
    payload = {
        "contents": [{
            "parts": [{"text": user_message}]
        }]
    }
    
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(GEMINI_API_URL, json=payload, headers=headers)
        response.raise_for_status() # Raise exception for HTTP errors
        
        result = response.json()
        
        # Extract the text from the Gemini response
        try:
            bot_reply = result['candidates'][0]['content']['parts'][0]['text']
        except (KeyError, IndexError):
            bot_reply = "I received a response, but I couldn't parse the structure."

        return jsonify({'reply': bot_reply})

    except requests.exceptions.RequestException as e:
        print(f"Error communicating with Gemini API: {e}")
        return jsonify({'error': 'Failed to communicate with AI provider.'}), 500

if __name__ == '__main__':
    # Run the Flask server
    app.run(host='0.0.0.0', port=8080, debug=True)
