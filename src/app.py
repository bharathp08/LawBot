from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configure Gemini API
api_key = 'AIzaSyB7hDhqN9PSs52d016llUP0SmN98pOhh5U'
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')

def get_legal_response(prompt):
    try:
        if prompt.lower().strip() in ['hello', 'hi', 'hey']:
            return "Hello! I'm KnowLawBot. Please describe your legal situation or question."
            
        enhanced_prompt = f"""As a legal expert specializing in Indian law, provide comprehensive advice for the following situation:
        
        {prompt}
        
        Structure your response as follows:
        TITLE: [Brief title describing the legal issue]
        INTRODUCTION: [Brief overview of the situation and applicable legal framework]
        1. RELEVANT INDIAN LAWS AND SECTIONS:
        2. POSSIBLE LEGAL ACTIONS:
        3. LEGAL REMEDIES AVAILABLE:
        4. IMPORTANT CONSIDERATIONS:
        
        DISCLAIMER: This information is for educational purposes only."""
            
        response = model.generate_content(enhanced_prompt)
        return response.text
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return "I apologize, but I'm having trouble. Please try again in a few moments."

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
        return jsonify({'error': 'An error occurred. Please try again.'}), 500

app = app