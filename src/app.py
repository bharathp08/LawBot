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

@app.route('/ask', methods=['POST'])
def ask():
    try:
        # Configure Gemini for each request in serverless environment
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')

        user_question = request.json.get('question')
        if not user_question:
            return jsonify({'response': 'Please ask a question'}), 200

        if user_question.lower().strip() in ['hello', 'hi', 'hey']:
            greeting = "Hello! I'm KnowLawBot, your Indian legal advisor. I can help you with questions about Indian laws, regulations, and legal matters. Please describe your legal concern."
            return jsonify({'response': greeting}), 200

        # Set a timeout for the model response
        start_time = time.time()
        max_time = 25  # Maximum time in seconds

        while time.time() - start_time < max_time:
            try:
                response = model.generate_content(
                    f"You are an Indian legal expert. Provide a clear and concise answer about: {user_question}. "
                    "Include specific laws, sections, and penalties if applicable."
                )
                
                if hasattr(response, 'text'):
                    return jsonify({'response': response.text}), 200
            except Exception as model_error:
                logging.error(f"Model error: {str(model_error)}")
                time.sleep(1)  # Wait before retry
                continue

        # If we reach here, we couldn't get a response within the timeout
        return jsonify({
            'response': 'I understand your question about legal matters. Please try asking again, and I will provide the information you need.'
        }), 200

    except Exception as e:
        logging.error(f"Request error: {str(e)}")
        return jsonify({
            'response': 'I am currently experiencing technical difficulties. Please try your question again.'
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