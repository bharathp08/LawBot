from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import logging
import os

# Update Flask app configuration
app = Flask(__name__)

# Configure logging with more details
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Configure Gemini API
api_key = 'AIzaSyB7hDhqN9PSs52d016llUP0SmN98pOhh5U'
genai.configure(api_key=api_key)

# Initialize model with retry mechanism
def get_model_instance():
    try:
        model = genai.GenerativeModel('gemini-pro')
        # Test the model
        test_response = model.generate_content("Test")
        logging.info("Model initialized successfully")
        return model
    except Exception as e:
        logging.error(f"Model initialization error: {str(e)}")
        return None

model = get_model_instance()

@app.route('/ask', methods=['POST'])
def ask():
    try:
        # Check if model is available
        if not model:
            logging.error("Model not initialized, attempting to reinitialize...")
            global model
            model = get_model_instance()
            if not model:
                return jsonify({'error': 'Service is starting up. Please try again in a few moments.'}), 503

        user_question = request.json.get('question')
        if not user_question:
            return jsonify({'error': 'No question provided'}), 400

        # Handle greetings
        if user_question.lower().strip() in ['hello', 'hi', 'hey']:
            greeting = "Hello! I'm KnowLawBot, your Indian legal advisor. I can help you with questions about Indian laws, regulations, and legal matters. Please describe your legal concern."
            return jsonify({'response': greeting})

        # Process legal questions with specific prompt and error handling
        try:
            prompt = """As an Indian legal expert, provide detailed information about: {question}. 
            Include:
            1. Relevant sections of law
            2. Specific penalties and fines
            3. Recent updates if any
            Format the response clearly with proper sections."""

            response = model.generate_content(prompt.format(question=user_question))
            
            if not response or not hasattr(response, 'text'):
                logging.error("Invalid response from model")
                return jsonify({'error': 'Unable to generate response. Please try again.'}), 503

            return jsonify({'response': response.text})

        except Exception as model_error:
            logging.error(f"Model generation error: {str(model_error)}")
            # Attempt to reinitialize model on error
            model = get_model_instance()
            return jsonify({'error': 'An error occurred. Please try your question again.'}), 503

    except Exception as e:
        logging.error(f"Request processing error: {str(e)}")
        return jsonify({'error': 'Service temporarily unavailable. Please try again later.'}), 503

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