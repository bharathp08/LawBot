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

# Initialize model with minimal configuration
try:
    model = genai.GenerativeModel('gemini-pro')
    
    # Test connection with simple prompt
    test_response = model.generate_content("Test")
    print("Model initialized successfully:", test_response.text)
    
except Exception as e:
    print(f"Initial model error: {str(e)}")
    try:
        # Try alternative initialization
        model = genai.GenerativeModel(
            model_name='gemini-pro',
            api_version='v1beta'
        )
        test_response = model.generate_content("Test")
        print("Connected with alternative configuration")
    except Exception as e:
        print(f"All attempts failed: {str(e)}")
        raise Exception("Unable to initialize Gemini model")

def get_legal_response(prompt):
    try:
        # Handle greetings
        if prompt.lower().strip() in ['hello', 'hi', 'hey']:
            return "Hello! I'm KnowLawBot, your Indian legal advisor. I can help you with questions about Indian laws, regulations, and legal matters. Please describe your legal concern."
        
        # Process legal questions
        enhanced_prompt = f"""As a legal expert specializing in Indian law, provide comprehensive advice for the following situation:
        
        {prompt}
        
        Structure your response as follows:
        TITLE: [Brief title describing the legal issue]
        INTRODUCTION: [Brief overview of the situation and applicable legal framework]
        1. RELEVANT INDIAN LAWS AND SECTIONS:
        [List specific sections of Motor Vehicles Act, IPC, or other relevant laws]
        2. POSSIBLE LEGAL ACTIONS:
        [Detail the legal consequences and procedures]
        3. LEGAL REMEDIES AVAILABLE:
        [Explain rights and options available]
        4. IMPORTANT CONSIDERATIONS:
        [Include key points about evidence, documentation, and time limits]
        
        DISCLAIMER: This information is for educational purposes only and should not be considered as legal advice."""
            
        response = model.generate_content(enhanced_prompt)
        if hasattr(response, 'text'):
            return response.text
        else:
            print("Response object:", response)
            return "I apologize, but I couldn't process your legal query. Please try rephrasing your question."
            
    except Exception as e:
        print(f"Error in get_legal_response: {str(e)}")
        return f"I apologize, but I'm experiencing technical difficulties: {str(e)}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        user_question = request.json.get('question')
        if not user_question:
            return jsonify({'error': 'No question provided'}), 400
        
        response = get_legal_response(user_question)
        return jsonify({'response': response})
    except Exception as e:
        print(f"Error in ask endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500

# For Vercel deployment
app = app