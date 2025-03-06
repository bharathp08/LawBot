from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import logging
import os

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Configure Gemini API
api_key = 'AIzaSyB7hDhqN9PSs52d016llUP0SmN98pOhh5U'
genai.configure(api_key=api_key)

def get_legal_response(question):
    try:
        model = genai.GenerativeModel('gemini-pro')
        
        # Construct a clear prompt for legal queries
        prompt = f"""As an Indian legal expert, provide a detailed answer about: {question}
        Include:
        1. Applicable laws and sections
        2. Penalties and consequences
        3. Recent amendments if any
        4. Important court judgments if relevant"""
        
        response = model.generate_content(prompt)
        if response and hasattr(response, 'text'):
            return response.text
        return None
    except Exception as e:
        logging.error(f"Model error: {str(e)}")
        return None

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

        # Get response from Gemini
        response = get_legal_response(user_question)
        if response:
            return jsonify({'response': response})
        
        # If no response, try one more time with simplified question
        simplified_response = get_legal_response(f"Explain Indian law regarding: {user_question}")
        if simplified_response:
            return jsonify({'response': simplified_response})
            
        return jsonify({'error': 'Unable to process request'}), 503

    except Exception as e:
        logging.error(f"Request error: {str(e)}")
        return jsonify({'response': 'I apologize, but I encountered an error. Please try asking your question again.'}), 200

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