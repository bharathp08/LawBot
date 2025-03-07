from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import logging
import os
from concurrent.futures import TimeoutError
import time

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Configure Gemini API
api_key = os.getenv('GOOGLE_API_KEY', 'AIzaSyB7hDhqN9PSs52d016llUP0SmN98pOhh5U')
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-pro')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        user_question = request.json.get('question')
        if not user_question:
            return jsonify({'response': 'Please ask a question'}), 200

        # Handle greetings
        if user_question.lower().strip() in ['hello', 'hi', 'hey']:
            greeting = "Hello! I'm KnowLawBot, your Indian legal advisor. I can help you with questions about Indian laws, regulations, and legal matters. Please describe your legal concern."
            return jsonify({'response': greeting})

        # Generate legal response
        prompt = f"""
        As an Indian legal expert, provide detailed information about: {user_question}
        Focus on:
        - Applicable laws and sections
        - Current penalties and fines
        - Legal procedures
        - Recent updates if any
        """
        
        response = model.generate_content(prompt)
        if hasattr(response, 'text'):
            return jsonify({'response': response.text}), 200
        
        return jsonify({
            'response': 'I apologize, but I could not generate a response. Please try rephrasing your question.'
        }), 200

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({
            'response': 'I am currently experiencing technical difficulties. Please try again in a moment.'
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