from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import logging
import os
from concurrent.futures import TimeoutError
import time

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

def get_model():
    try:
        api_key = os.getenv('GOOGLE_API_KEY', 'AIzaSyB7hDhqN9PSs52d016llUP0SmN98pOhh5U')
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-pro')
    except Exception as e:
        logging.error(f"Model initialization error: {str(e)}")
        return None

@app.route('/ask', methods=['POST'])
def ask():
    try:
        user_question = request.json.get('question')
        if not user_question:
            return jsonify({'response': 'Please ask a question'}), 200

        if user_question.lower().strip() in ['hello', 'hi', 'hey']:
            greeting = "Hello! I'm KnowLawBot, your Indian legal advisor. I can help you with questions about Indian laws, regulations, and legal matters. Please describe your legal concern."
            return jsonify({'response': greeting})

        model = get_model()
        if not model:
            return jsonify({'response': 'Service temporarily unavailable. Please try again.'}), 200

        prompt = f"""
        You are an Indian legal expert. Provide a clear and detailed answer about: {user_question}
        Include:
        1. Specific sections of applicable laws
        2. Current penalties and fines
        3. Legal procedures
        4. Recent amendments if any
        Format the response with proper sections and bullet points.
        """

        response = model.generate_content(prompt, generation_config={
            'temperature': 0.7,
            'top_p': 0.8,
            'top_k': 40,
            'max_output_tokens': 2048,
        })

        if hasattr(response, 'text'):
            return jsonify({'response': response.text}), 200
        
        return jsonify({
            'response': 'I apologize, but I could not generate a response. Please try rephrasing your question.'
        }), 200

    except Exception as e:
        logging.error(f"Request error: {str(e)}")
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