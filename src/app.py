from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Configure Gemini API
api_key = 'AIzaSyB7hDhqN9PSs52d016llUP0SmN98pOhh5U'
genai.configure(api_key=api_key)

# Single model initialization
model = None
try:
    model = genai.GenerativeModel(
        model_name='gemini-pro',
        generation_config={
            "temperature": 0.7,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }
    )
    # Verify model initialization
    test_response = model.generate_content("Test connection")
    logging.info("Model initialized and tested successfully")
except Exception as e:
    logging.error(f"Model initialization error: {str(e)}")

@app.route('/ask', methods=['POST'])
def ask():
    if model is None:
        logging.error("Model not initialized")
        return jsonify({'error': 'Service unavailable'}), 503

    try:
        user_question = request.json.get('question')
        if not user_question:
            return jsonify({'error': 'No question provided'}), 400

        # Handle greetings
        if user_question.lower().strip() in ['hello', 'hi', 'hey']:
            greeting = "Hello! I'm KnowLawBot, your Indian legal advisor. I can help you with questions about Indian laws, regulations, and legal matters. Please describe your legal concern."
            return jsonify({'response': greeting})

        # Process legal questions with error handling
        try:
            response = model.generate_content(user_question)
            if hasattr(response, 'text'):
                return jsonify({'response': response.text})
            else:
                logging.error("Invalid response format")
                return jsonify({'error': 'Invalid response from model'}), 500
        except Exception as e:
            logging.error(f"Content generation error: {str(e)}")
            return jsonify({'error': 'Failed to generate response'}), 500
            
    except Exception as e:
        logging.error(f"Request processing error: {str(e)}")
        return jsonify({'error': 'Service temporarily unavailable'}), 503
if __name__ == '__main__':
    app.run(debug=False)