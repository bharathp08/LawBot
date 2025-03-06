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

# Initialize model with specific configuration
model = genai.GenerativeModel(
    model_name='gemini-pro',
    generation_config={
        "temperature": 0.7,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }
)

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
        enhanced_prompt = f"""As an Indian legal expert, provide advice about: {user_question}
        Focus on relevant laws, penalties, and legal consequences."""

        response = model.generate_content(enhanced_prompt)
        return jsonify({'response': response.text})
        
    except Exception as e:
        logging.error(f"Request processing error: {str(e)}")
        return jsonify({'error': 'Service temporarily unavailable'}), 503
if __name__ == '__main__':
    app.run(debug=False)