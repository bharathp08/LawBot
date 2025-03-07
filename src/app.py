from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import logging
import os
from concurrent.futures import TimeoutError
import time

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Configure Gemini API
api_key = 'AIzaSyB7hDhqN9PSs52d016llUP0SmN98pOhh5U'
genai.configure(api_key=api_key)

# Create a persistent model instance
model = genai.GenerativeModel('gemini-pro')

# Cache for storing recent responses
response_cache = {}

@app.route('/ask', methods=['POST'])
def ask():
    try:
        user_question = request.json.get('question')
        if not user_question:
            return jsonify({'response': 'Please ask a question'}), 200

        # Check cache first
        cache_key = user_question.lower().strip()
        if cache_key in response_cache:
            return jsonify({'response': response_cache[cache_key]}), 200

        if cache_key in ['hello', 'hi', 'hey']:
            greeting = "Hello! I'm KnowLawBot, your Indian legal advisor. I can help you with questions about Indian laws, regulations, and legal matters. Please describe your legal concern."
            return jsonify({'response': greeting}), 200

        # Generate response
        response = model.generate_content(
            f"You are an Indian legal expert. Provide a clear and concise answer about: {user_question}. "
            "Include specific laws, sections, and penalties if applicable."
        )

        if hasattr(response, 'text'):
            # Cache the response
            response_cache[cache_key] = response.text
            # Limit cache size
            if len(response_cache) > 100:
                # Remove oldest entries
                keys = list(response_cache.keys())
                for old_key in keys[:50]:
                    response_cache.pop(old_key)
            
            return jsonify({'response': response.text}), 200

        return jsonify({
            'response': 'I understand your question. Please try rephrasing it for a better response.'
        }), 200

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({
            'response': 'I am currently processing multiple requests. Please try again in a moment.'
        }), 200

@app.route('/')
def home():
    return render_template('index.html')

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Page not found'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500
# Remove the if __name__ == '__main__' block for Vercel deployment