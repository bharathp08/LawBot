from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import logging
import os

# Update Flask app configuration
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Configure Gemini API
api_key = 'AIzaSyB7hDhqN9PSs52d016llUP0SmN98pOhh5U'
genai.configure(api_key=api_key)

# Initialize model
model = genai.GenerativeModel('gemini-pro')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        user_question = request.json.get('question')
        if not user_question:
            return jsonify({'error': 'No question provided'}), 400

        # Handle greetings
        if user_question.lower().strip() in ['hello', 'hi', 'hey']:
            greeting = "Hello! I'm KnowLawBot, your Indian legal advisor. I can help you with questions about Indian laws, regulations, and legal matters. Please describe your legal concern."
            return jsonify({'response': greeting})

        # Process legal questions with specific prompt
        prompt = """As an Indian legal expert, provide detailed information about: {question}. 
        Include:
        1. Relevant sections of law
        2. Specific penalties and fines
        3. Recent updates if any
        Format the response clearly with proper sections."""

        response = model.generate_content(prompt.format(question=user_question))
        return jsonify({'response': response.text})

    except Exception as e:
        logging.error(f"Request error: {str(e)}")
        return jsonify({'error': 'Service temporarily unavailable'}), 503

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