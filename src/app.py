from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Configure Gemini API
api_key = 'AIzaSyB7hDhqN9PSs52d016llUP0SmN98pOhh5U'
genai.configure(api_key=api_key)

# Initialize model with safety settings
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
        legal_prompt = f"""As an Indian legal expert, please provide information about: {user_question}
        Include:
        1. Relevant sections of Indian law
        2. Applicable fines and penalties
        3. Legal consequences
        4. Important considerations
        """
        
        response = model.generate_content(legal_prompt)
        return jsonify({'response': response.text})
            
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({'error': 'Unable to process request'}), 500
# Add route for root path
@app.route('/')
def home():
    try:
        return render_template('index.html')
    except Exception as e:
        logging.error(f"Error rendering template: {str(e)}")
        return "Service temporarily unavailable", 503

# Add error handler for 404
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Page not found'}), 404

# Add error handler for 500
@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500
if __name__ == '__main__':
    app.run(debug=False)