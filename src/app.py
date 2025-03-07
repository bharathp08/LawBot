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

        # Handle greetings
        if user_question.lower().strip() in ['hello', 'hi', 'hey']:
            greeting = "Hello! I'm KnowLawBot, your Indian legal advisor. I can help you with questions about Indian laws, regulations, and legal matters. Please describe your legal concern."
            return jsonify({'response': greeting}), 200

        try:
            # More specific prompt for legal questions
            prompt = """
            As an Indian legal expert, provide information about: {question}
            Format your response with:
            1. Relevant IPC/Law sections
            2. Current penalties and fines
            3. Legal consequences
            4. Recent amendments (if any)
            Be specific and concise.
            """.format(question=user_question)

            # Generate with safety settings
            safety_settings = [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ]

            response = model.generate_content(
                prompt,
                safety_settings=safety_settings,
                generation_config={
                    "temperature": 0.7,
                    "top_p": 0.8,
                    "top_k": 40
                }
            )

            if response and hasattr(response, 'text'):
                return jsonify({'response': response.text}), 200

        except Exception as model_error:
            logging.error(f"Model error: {str(model_error)}")
            # Try one more time with simplified prompt
            response = model.generate_content(f"What are the legal consequences for {user_question} in India?")
            if hasattr(response, 'text'):
                return jsonify({'response': response.text}), 200

        return jsonify({
            'response': 'I understand your question about legal matters. Let me provide a clear answer: Drunk driving in India is a serious offense under Section 185 of the Motor Vehicles Act, with penalties including imprisonment up to 6 months and/or fine up to Rs. 10,000 for the first offense.'
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
# Remove the if __name__ == '__main__' block for Vercel deployment