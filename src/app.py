from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import logging
import os

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Get API key from environment variable
api_key = os.getenv('GEMINI_API_KEY', 'AIzaSyB7hDhqN9PSs52d016llUP0SmN98pOhh5U')

def initialize_gemini():
    try:
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        logging.error(f"Gemini configuration error: {str(e)}")
        return False

def get_response(question):
    try:
        model = genai.GenerativeModel('gemini-pro')
        prompt = """You are an Indian legal expert. Provide a clear and detailed response about: {question}
        Focus on:
        - Specific sections of Indian law that apply
        - Current penalties and fines
        - Recent legal updates or amendments
        - Important considerations"""
        
        response = model.generate_content(prompt.format(question=question))
        return response.text if hasattr(response, 'text') else None
    except Exception as e:
        logging.error(f"Response generation error: {str(e)}")
        return None

@app.route('/ask', methods=['POST'])
def ask():
    if not initialize_gemini():
        return jsonify({'error': 'Service initialization failed'}), 503

    try:
        user_question = request.json.get('question')
        if not user_question:
            return jsonify({'error': 'No question provided'}), 400

        if user_question.lower().strip() in ['hello', 'hi', 'hey']:
            greeting = "Hello! I'm KnowLawBot, your Indian legal advisor. I can help you with questions about Indian laws, regulations, and legal matters. Please describe your legal concern."
            return jsonify({'response': greeting})

        response_text = get_response(user_question)
        if response_text:
            return jsonify({'response': response_text})
        return jsonify({'error': 'Unable to generate response'}), 503

    except Exception as e:
        logging.error(f"Request error: {str(e)}")
        return jsonify({'error': 'Service error'}), 503

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