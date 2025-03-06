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

# Initialize model with safety settings
def get_model_instance():
    try:
        model = genai.GenerativeModel('gemini-pro')
        generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }
        model.generation_config = generation_config
        return model
    except Exception as e:
        logging.error(f"Model initialization error: {str(e)}")
        return None

model = get_model_instance()

@app.route('/ask', methods=['POST'])
def ask():
    try:
        if not model:
            global model
            model = get_model_instance()
            if not model:
                return jsonify({'error': 'Unable to initialize service. Please try again later.'}), 503

        user_question = request.json.get('question')
        if not user_question:
            return jsonify({'error': 'No question provided'}), 400

        # Handle greetings
        if user_question.lower().strip() in ['hello', 'hi', 'hey']:
            greeting = "Hello! I'm KnowLawBot, your Indian legal advisor. I can help you with questions about Indian laws, regulations, and legal matters. Please describe your legal concern."
            return jsonify({'response': greeting})

        # Process legal questions with improved prompt
        try:
            prompt = """You are an Indian legal expert. Provide a clear and detailed response about: {question}
            Focus on:
            - Specific sections of Indian law that apply
            - Current penalties and fines
            - Recent legal updates or amendments
            - Important considerations
            
            Format the response in clear sections with proper headings."""

            response = model.generate_content(prompt.format(question=user_question))
            
            if hasattr(response, 'text'):
                return jsonify({'response': response.text})
            else:
                return jsonify({'error': 'Unable to generate response'}), 503

        except Exception as model_error:
            logging.error(f"Generation error: {str(model_error)}")
            return jsonify({'error': 'Unable to process your question. Please try again.'}), 503

    except Exception as e:
        logging.error(f"Request error: {str(e)}")
        return jsonify({'error': 'Service error. Please try again later.'}), 503

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