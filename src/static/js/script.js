document.addEventListener('DOMContentLoaded', function() {
    const questionForm = document.getElementById('questionForm');
    const questionInput = document.getElementById('questionInput');
    const sendButton = document.getElementById('sendButton');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const chatMessages = document.getElementById('chatMessages');

    // Auto-resize textarea as user types
    questionInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight < 120) ? this.scrollHeight + 'px' : '120px';
    });

    // Add the missing scrollToBottom function
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Function to handle sending messages
    async function sendMessage() {
        const question = questionInput.value.trim();
        if (!question) {
            return;
        }
    
        // Add user message to chat
        addMessage(question, 'user');
        
        // Clear input and reset height
        questionInput.value = '';
        questionInput.style.height = 'auto';
        
        // Show loading indicator
        loadingIndicator.classList.remove('hidden');
        
        try {
            const response = await fetch('/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ question: question })
            });
    
            const data = await response.json();
            
            // Hide loading indicator
            loadingIndicator.classList.add('hidden');
            
            if (response.ok && data.response) {
                // Add bot response to chat
                addMessage(data.response, 'bot');
            } else {
                // Show a more user-friendly error message
                const errorMessage = "I apologize, but I'm having trouble processing your request at the moment. " +
                               "Please try rephrasing your question or try again in a few moments.";
                addMessage(errorMessage, 'bot');
            }
        } catch (error) {
            console.error('Error:', error);
            loadingIndicator.classList.add('hidden');
            const errorMessage = "I apologize for the inconvenience. There seems to be a technical issue. " +
                           "Please try again in a few moments.";
            addMessage(errorMessage, 'bot');
        }
        
        // Scroll to bottom of chat
        scrollToBottom();
    }
    function formatResponse(text) {
        if (!text) return '';
        
        try {
            // Replace section titles with styled headings
            text = text.replace(/TITLE:/g, '<h4 class="response-title">');
            text = text.replace(/INTRODUCTION:/g, '</h4><p class="response-intro">');
            
            // Format numbered sections
            text = text.replace(/(\d+)\.\s+([A-Z\s]+):/g, '</p><h5>$1. $2:</h5>');
            
            // Format disclaimer
            text = text.replace(/DISCLAIMER:/g, '<hr><p class="disclaimer"><strong>Disclaimer:</strong>');
            
            // Convert bullet points and handle line breaks
            text = text.replace(/[-*]\s+/g, '<li>');
            text = text.replace(/\n\n/g, '</p><p>');
            text = text.replace(/\n/g, '<br>');
            
            // Ensure proper closing tags
            if (!text.endsWith('</p>')) {
                text = text + '</p>';
            }
            
            return text;
        } catch (error) {
            console.error('Error formatting response:', error);
            return text; // Return original text if formatting fails
        }
    }
    // Fix form submission
    if (questionForm) {
        questionForm.addEventListener('submit', function(e) {
            e.preventDefault();
            sendMessage();
        });
    }
    
    // Add event listeners
    if (sendButton) {
        sendButton.addEventListener('click', sendMessage);
    }
    
    // Fix Enter key handling
    questionInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const avatarDiv = document.createElement('div');
        avatarDiv.className = 'message-avatar';
        
        const icon = document.createElement('i');
        if (sender === 'bot') {
            icon.className = 'fas fa-balance-scale';
        } else {
            icon.className = 'fas fa-user';
        }
        
        avatarDiv.appendChild(icon);
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        if (sender === 'bot') {
            // Format the bot response
            text = formatResponse(text);
            contentDiv.innerHTML = text;
        } else {
            const paragraph = document.createElement('p');
            paragraph.textContent = text;
            contentDiv.appendChild(paragraph);
        }
        
        messageDiv.appendChild(avatarDiv);
        messageDiv.appendChild(contentDiv);
        
        chatMessages.appendChild(messageDiv);
    }
    // Initial scroll to bottom
    scrollToBottom();
});