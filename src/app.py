from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configure Gemini API
api_key = 'AIzaSyB7hDhqN9PSs52d016llUP0SmN98pOhh5U'
genai.configure(api_key=api_key)

try:
    # Simple model initialization
    model = genai.GenerativeModel('gemini-pro')
    
    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/ask', methods=['POST'])
    def ask():
        try:
            user_question = request.json.get('question')
            if not user_question:
                return jsonify({'error': 'No question provided'}), 400

            # Generate response
            response = model.generate_content(user_question)
            return jsonify({'response': response.text})
            
        except Exception as e:
            print(f"Error in ask endpoint: {str(e)}")
            return jsonify({'error': 'Unable to process request'}), 500

except Exception as e:
    print(f"Model initialization failed: {str(e)}")

# For Vercel deployment
app = app