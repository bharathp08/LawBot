import gradio as gr
import google.generativeai as genai
import os

# Configure Gemini API
api_key = os.getenv('GOOGLE_API_KEY', 'AIzaSyB7hDhqN9PSs52d016llUP0SmN98pOhh5U')
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')

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

def get_legal_response(message, history):
    if not message:
        return "Please ask a question about Indian law."
    
    # Handle greetings
    if message.lower().strip() in ['hello', 'hi', 'hey']:
        return "Hello! I'm KnowLawBot, your Indian legal advisor. I can help you with questions about Indian laws, regulations, and legal matters. Please describe your legal concern."
    
    # Generate legal response
    prompt = f"""
    As an Indian legal expert, provide detailed information about: {message}
    Focus on:
    1. Applicable laws and sections
    2. Current penalties and fines
    3. Legal procedures
    4. Recent amendments if any
    Format your response clearly with headings and bullet points where appropriate.
    """
    
    try:
        response = model.generate_content(prompt)
        if hasattr(response, 'text'):
            return response.text
        return "I apologize, but I could not generate a response. Please try rephrasing your question."
    except Exception as e:
        print(f"Error: {str(e)}")
        return "I am currently experiencing technical difficulties. Please try again in a moment."

# Create Gradio Interface
with gr.Blocks(css=custom_css) as demo:
    gr.HTML("""
    <div class="chat-header">
        <h1>KnowLawBot - Indian Legal Advisor</h1>
        <p>Get expert advice on Indian law for your legal questions</p>
    </div>
    """)
    
    chatbot = gr.Chatbot(
        label="Chat with KnowLawBot",
        bubble_full_width=False,
        height=500,
        avatar_images=(None, "https://img.icons8.com/color/96/000000/scales--v1.png")
    )
    
    msg = gr.Textbox(
        placeholder="Ask about Indian laws, regulations, or legal procedures...",
        label="Your Question",
        scale=9
    )
    
    clear = gr.Button("Clear Chat", scale=1)
    
    msg.submit(
        get_legal_response,
        [msg, chatbot],
        [chatbot],
        clear_input=True
    )
    
    clear.click(lambda: None, None, chatbot, queue=False)

# Launch the app
if __name__ == "__main__":
    demo.launch()