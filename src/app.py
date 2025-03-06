from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import logging

# Update Flask app configuration
app = Flask(__name__, 
    template_folder='c:/Users/Bharth/OneDrive/Desktop/ByteSquad/templates'
)
logging.basicConfig(level=logging.INFO)

# Configure Gemini API and model
api_key = 'AIzaSyB7hDhqN9PSs52d016llUP0SmN98pOhh5U'
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')

def get_model_response(prompt):
    try:
        # Direct response generation
        response = model.generate_content(prompt)
        return response.text if hasattr(response, 'text') else None
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

        # Process legal questions with simple prompt
        response_text = get_model_response(user_question)
        
        if response_text:
            return jsonify({'response': response_text})
        
        return jsonify({'error': 'Unable to generate response'}), 503
            
    except Exception as e:
        logging.error(f"Request error: {str(e)}")
        return jsonify({'error': 'Service temporarily unavailable'}), 503

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