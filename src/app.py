from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configure Gemini API with beta version
api_key = 'AIzaSyB7hDhqN9PSs52d016llUP0SmN98pOhh5U'
genai.configure(api_key=api_key, api_version='v1beta')

# Single model initialization with all configurations
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# Configure Gemini API
api_key = 'AIzaSyB7hDhqN9PSs52d016llUP0SmN98pOhh5U'
genai.configure(api_key=api_key)

# Global model variable
model = None

def initialize_model():
    global model
    try:
        model = genai.GenerativeModel('gemini-pro')
        # Test the model
        test_response = model.generate_content("Test")
        return True
    except Exception as e:
        print(f"Model initialization error: {str(e)}")
        return False

# Initialize model when app starts
if not initialize_model():
    print("Failed to initialize model")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    global model
    try:
        # Check if model is initialized
        if model is None and not initialize_model():
            return jsonify({'error': 'Model not available'}), 503
            
        user_question = request.json.get('question')
        if not user_question:
            return jsonify({'error': 'No question provided'}), 400
        
        response = get_legal_response(user_question)
        return jsonify({'response': response})
    except Exception as e:
        print(f"Error in ask endpoint: {str(e)}")
        return jsonify({'error': 'An error occurred processing your request'}), 500

# For Vercel deployment
app = app