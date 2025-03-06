from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv
import time
from tenacity import retry, stop_after_attempt, wait_exponential

load_dotenv()

app = Flask(__name__)

# Configure Gemini API
try:
    # Use the API key directly
    api_key = 'AIzaSyB7hDhqN9PSs52d016llUP0SmN98pOhh5U'
    
    # Configure with specific settings
    genai.configure(api_key=api_key)
    
    # List available models to find the correct one
    models = genai.list_models()
    print("Available models:", [model.name for model in models])
    
    # Use a model that's definitely available
    model = genai.GenerativeModel('gemini-1.5-pro')
    
    # Test the API connection
    test_response = model.generate_content("Test connection")
    print("Gemini API connected successfully")
except Exception as e:
    print(f"Error configuring Gemini API: {str(e)}")
    # We'll continue and handle errors in the routes

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def get_legal_response(prompt):
    try:
        # Add error checking for simple greetings first
        if prompt.lower().strip() in ['hello', 'hi', 'hey']:
            return "Hello! I'm KnowLawBot. Please describe your legal situation or question, and I'll provide detailed information about relevant Indian laws and possible actions."
            
        enhanced_prompt = f"""As a legal expert specializing in Indian law, provide comprehensive advice for the following situation:
        
        {prompt}
        
        Structure your response as follows:
        
        TITLE: [Brief title describing the legal issue]
        
        INTRODUCTION: [Brief overview of the situation and applicable legal framework]
        
        1. RELEVANT INDIAN LAWS AND SECTIONS:
        [List the specific laws, acts, and sections that apply to this situation]
        
        2. POSSIBLE LEGAL ACTIONS:
        [Outline the legal actions that can be taken]
        
        3. LEGAL REMEDIES AVAILABLE:
        [Describe the remedies available under Indian law]
        
        4. IMPORTANT CONSIDERATIONS:
        [Highlight key factors, limitations, or special considerations]
        
        DISCLAIMER: This information is for educational purposes only and does not constitute legal advice. Please consult with a qualified legal professional for advice specific to your situation.
        """
            
        response = model.generate_content(enhanced_prompt)
        if response and response.text:
            return response.text
        else:
            return "I apologize, but I couldn't generate a proper response. Please try rephrasing your question."
            
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        return "I apologize, but I'm having trouble processing your request. Please try again with a more specific legal question."
        return f"Sorry, I encountered an error while processing your request. Please try again in a few moments."

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

if __name__ == '__main__':
    app.run(debug=True)

# This line is needed for Vercel deployment
app = app