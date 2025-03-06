from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import logging
import os

# Update Flask app configuration
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Configure Gemini API with safety settings
api_key = 'AIzaSyB7hDhqN9PSs52d016llUP0SmN98pOhh5U'  # Use direct key for testing
genai.configure(api_key=api_key)

# Initialize model with verification
model = None
try:
    # Initialize with specific model
    model = genai.GenerativeModel('gemini-pro')
    
    # Set specific parameters for the model
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    ]
    
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.8,
        "top_k": 40,
        "max_output_tokens": 2048,
    }
    
    # Test the model with simple prompt
    response = model.generate_content(
        "Test connection",
        safety_settings=safety_settings,
        generation_config=generation_config
    )
    
    if response.text:
        logging.info("Model initialized successfully")
    else:
        raise Exception("Model response empty")

except Exception as e:
    logging.error(f"Model initialization failed: {str(e)}")
    model = None

@app.route('/ask', methods=['POST'])
def ask():
    if not model:
        return jsonify({'error': 'Model not initialized. Please try again later.'}), 503
        
    try:
        user_question = request.json.get('question')
        if not user_question:
            return jsonify({'error': 'No question provided'}), 400

        # Handle greetings
        if user_question.lower().strip() in ['hello', 'hi', 'hey']:
            greeting = "Hello! I'm KnowLawBot, your Indian legal advisor. I can help you with questions about Indian laws, regulations, and legal matters. Please describe your legal concern."
            return jsonify({'response': greeting})

        # Process legal questions
        response = model.generate_content(
            f"As an Indian legal expert, provide information about: {user_question}. Include relevant laws and penalties."
        )
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