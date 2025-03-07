from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import logging
import os

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Configure Gemini API
api_key = 'AIzaSyB7hDhqN9PSs52d016llUP0SmN98pOhh5U'
genai.configure(api_key=api_key)

# Initialize model once
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

        # Process legal questions
        prompt = f"""As an Indian legal expert, provide a detailed answer about: {user_question}
        Focus on:
        - Relevant laws and sections
        - Penalties and fines
        - Recent legal updates
        - Important considerations"""

        response = model.generate_content(prompt)
        
        if response and hasattr(response, 'text'):
            return jsonify({'response': response.text})
        else:
            logging.error("Invalid response from model")
            return jsonify({'response': 'I apologize, but I could not process your question. Please try again.'})

    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        return jsonify({'response': 'I apologize for the inconvenience. Please try asking your question again.'})

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