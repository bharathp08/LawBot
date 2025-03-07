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
        # Use a direct API key for testing
        api_key = 'AIzaSyB7hDhqN9PSs52d016llUP0SmN98pOhh5U'
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        # Test the model immediately
        test_response = model.generate_content("Test connection")
        if not hasattr(test_response, 'text'):
            raise Exception("Model connection failed")
            
        return model
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
            return jsonify({'response': 'Unable to connect to the legal assistant. Please try again.'}), 200

        # Simplified prompt for better response
        prompt = f"""As an Indian legal expert, explain the laws and penalties for: {user_question}
        Include specific sections, fines, and recent updates."""

        try:
            response = model.generate_content(prompt)
            if hasattr(response, 'text'):
                return jsonify({'response': response.text}), 200
        except Exception as e:
            logging.error(f"Generation error: {str(e)}")
            # Try one more time with a simpler prompt
            try:
                response = model.generate_content(f"What are the Indian laws regarding {user_question}?")
                if hasattr(response, 'text'):
                    return jsonify({'response': response.text}), 200
            except:
                pass
        
        return jsonify({
            'response': 'I apologize, but I could not retrieve the legal information. Please try asking in a different way.'
        }), 200

    except Exception as e:
        logging.error(f"Request error: {str(e)}")
        return jsonify({
            'response': 'The service is temporarily unavailable. Please try again in a moment.'
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