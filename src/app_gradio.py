import gradio as gr
import google.generativeai as genai
import os

# Configure Gemini API with proper error handling
api_key = os.getenv('GOOGLE_API_KEY')  # Will be set in Hugging Face Space settings
genai.configure(api_key=api_key)

def get_response(message):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Strict check for legal queries
        legal_prompt = f"""
        You are an Indian Legal System Validator.
        Query: '{message}'
        
        Strictly check if this query is about:
        - Indian Constitution
        - Indian Laws and Acts
        - Legal procedures in India
        - Indian Court systems
        - Legal rights in India
        - Criminal or Civil procedures in India
        
        Respond ONLY with 'YES' if related to Indian legal system, or 'NO' for anything else.
        """
        check_response = model.generate_content(legal_prompt)
        is_legal = check_response.text.strip().upper() == 'YES'
        
        if not is_legal:
            return "I am KnowLawBot, specialized in Indian legal matters only. Please ask questions about Indian laws, constitution, legal procedures, or your legal rights in India. For other topics, please consult appropriate resources."
        
        # Enhanced legal response prompt
        prompt = f"""
        You are KnowLawBot, an expert specifically in Indian Law and Constitution.
        
        Query: {message}
        
        Provide a detailed response STRICTLY based on Indian legal framework:
        1. Relevant Indian Laws and Constitutional Articles
        2. Specific Sections and Provisions
        3. Legal Interpretation by Indian Courts
        4. Applicable Procedures and Requirements
        5. Recent Supreme Court or High Court Judgments
        
        Important Guidelines:
        - Only provide information from Indian legal sources
        - Cite specific laws, sections, and articles
        - Include recent amendments if applicable
        - Focus on practical legal information
        - If unsure about any aspect, mention it clearly
        
        Format the response with clear headings and bullet points.
        """
        
        response = model.generate_content(prompt)
        return response.text if hasattr(response, 'text') else "Sorry, I couldn't generate a response."
    except Exception as e:
        print(f"Error: {str(e)}")
        return "I apologize, but I'm having trouble accessing the legal database. Please try again in a moment."
        return "I apologize, but I'm having trouble connecting to the legal database. Please try again in a moment."

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