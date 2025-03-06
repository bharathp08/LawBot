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
        return True
    except Exception as e:
        print(f"Model initialization error: {str(e)}")
        return False

def get_legal_response(prompt):
    global model
    try:
        # Handle greetings
        if prompt.lower().strip() in ['hello', 'hi', 'hey']:
            return "Hello! I'm KnowLawBot, your Indian legal advisor. I can help you with questions about Indian laws, regulations, and legal matters. Please describe your legal concern."
        
        # Process legal questions
        enhanced_prompt = f"""As a legal expert specializing in Indian law, provide comprehensive advice for the following situation:
        {prompt}"""
            
        response = model.generate_content(enhanced_prompt)
        return response.text if hasattr(response, 'text') else "I apologize, but I couldn't process your legal query."
            
    except Exception as e:
        print(f"Error in get_legal_response: {str(e)}")
        return "I apologize, but I'm experiencing technical difficulties. Please try again later."

@app.route('/ask', methods=['POST'])
def ask():
    try:
        if model is None and not initialize_model():
            return jsonify({'error': 'Service temporarily unavailable'}), 503
            
        user_question = request.json.get('question')
        if not user_question:
            return jsonify({'error': 'No question provided'}), 400
        
        response = get_legal_response(user_question)
        return jsonify({'response': response})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
        return jsonify({'error': 'An error occurred processing your request'}), 500

# For Vercel deployment
app = app