import gradio as gr
import google.generativeai as genai
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Configure Gemini API
api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=api_key)

def initialize_model():
    try:
        models = list(genai.list_models())
        preferred_model = 'gemini-1.5-flash'
        for model_info in models:
            if preferred_model in model_info.name:
                return genai.GenerativeModel(model_info.name)
        return genai.GenerativeModel('gemini-pro')
    except Exception as e:
        logging.error(f"Model initialization error: {str(e)}")
        return None

def get_response(message):
    try:
        model = initialize_model()
        if not model:
            return "System initialization error. Please try again later."

        # Enhanced legal validation prompt
        validation_prompt = f"""
        Strictly validate if this query relates to Indian legal system:
        Query: '{message}'
        
        Valid topics:
        - Indian Constitution and amendments
        - Indian Penal Code (IPC)
        - Civil and Criminal laws of India
        - Indian court procedures
        - Legal rights under Indian law
        - Supreme Court/High Court judgments
        - Indian legal procedures and documentation
        
        Respond only with 'YES' or 'NO'.
        Any non-legal or non-Indian legal topics must return 'NO'.
        """
        
        validation = model.generate_content(validation_prompt)
        if validation.text.strip().upper() != 'YES':
            return "I can only provide information about Indian laws, constitution, and legal procedures. Please ask a question related to Indian legal matters."

        # Enhanced legal response prompt
        legal_prompt = f"""
        You are an Indian Legal Expert Bot. Provide information strictly based on Indian law for: {message}
        
        Required format:
        1. Applicable Laws:
           - Relevant acts and sections
           - Constitutional provisions
        
        2. Legal Details:
           - Specific provisions
           - Current interpretations
           - Relevant case laws
        
        3. Procedures (if applicable):
           - Step-by-step process
           - Required documentation
           - Timeframes
        
        4. Recent Updates:
           - Latest amendments
           - Supreme Court judgments
        
        Strict Guidelines:
        - Only cite Indian legal sources
        - Include section numbers and act names
        - Mention recent relevant judgments
        - If information is unclear, state it
        """

        response = model.generate_content(legal_prompt)
        return response.text if hasattr(response, 'text') else "Error generating response"
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return "I apologize, but I'm having trouble accessing the legal database. Please try again."

# Custom CSS for better UI
custom_css = """
.gradio-container {
    font-family: 'Poppins', sans-serif;
}
.chat-message-container {
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 10px;
}
.user-message {
    background-color: #e6f7ff;
    border-left: 5px solid #1890ff;
}
.bot-message {
    background-color: #f6f6f6;
    border-left: 5px solid #722ed1;
}
.chat-header {
    text-align: center;
    padding: 20px;
    background: linear-gradient(135deg, #722ed1 0%, #1890ff 100%);
    color: white;
    border-radius: 10px;
    margin-bottom: 20px;
}
"""

# Create simple interface
with gr.Blocks(css=custom_css) as demo:
    gr.HTML("""
    <div class="chat-header">
        <h1>KnowLawBot - Indian Legal Advisor</h1>
        <p>Get expert advice on Indian law for your legal questions</p>
    </div>
    """)
    
    chatbot = gr.Chatbot(
        value=[],
        elem_id="chatbot",
        height=400
    )
    
    msg = gr.Textbox(
        placeholder="Ask about Indian laws, regulations, or legal procedures...",
        label="Your Question",
        elem_id="user-input"
    )
    
    clear = gr.Button("Clear Chat")
    
    def user_input(user_message, history):
        if not user_message:
            return "", history
        bot_response = get_response(user_message)
        history = history + [(user_message, bot_response)]
        return "", history
    
    msg.submit(user_input, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: None, None, chatbot, queue=False)

if __name__ == "__main__":
    demo.launch(share=True)  # Added share=True for better accessibility