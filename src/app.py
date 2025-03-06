from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Configure Gemini API
api_key = 'AIzaSyB7hDhqN9PSs52d016llUP0SmN98pOhh5U'
genai.configure(api_key=api_key)

# Initialize model outside of route handlers
try:
    model = genai.GenerativeModel('gemini-pro')
    logging.info("Gemini model initialized successfully")
except Exception as e:
    logging.error(f"Failed to initialize Gemini model: {str(e)}")
    model = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    if model is None:
        return jsonify({'error': 'Service unavailable'}), 503

    try:
        user_question = request.json.get('question')
        if not user_question:
            return jsonify({'error': 'No question provided'}), 400

        # Generate response with timeout
        response = model.generate_content(user_question, timeout=30)
        
        if not hasattr(response, 'text'):
            return jsonify({'error': 'Invalid response from model'}), 500
            
        return jsonify({'response': response.text})
        
    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        return jsonify({'error': 'Unable to process request'}), 500

if __name__ == '__main__':
    app.run(debug=False)