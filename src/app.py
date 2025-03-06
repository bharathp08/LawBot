from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configure Gemini API
api_key = 'AIzaSyB7hDhqN9PSs52d016llUP0SmN98pOhh5U'
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.0-pro')  # Updated model name

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