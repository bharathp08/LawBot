function startChat() {
    const userName = document.getElementById('userName').value.trim();
    if (!userName) {
        alert('Please enter your name to continue');
        return;
    }

    document.getElementById('welcome-screen').classList.add('hidden');
    document.getElementById('chat-screen').classList.remove('hidden');
    document.getElementById('userGreeting').textContent = `Hello, ${userName}!`;
}

function sendMessage() {
    const userInput = document.getElementById('userInput');
    const chatContainer = document.getElementById('chatContainer');
    const question = userInput.value.trim();

    if (!question) return;

    // Add user message
    const userMessage = document.createElement('div');
    userMessage.className = 'message user-message';
    userMessage.textContent = question;
    chatContainer.appendChild(userMessage);

    // Clear input
    userInput.value = '';

    // Add loading message
    const loadingMessage = document.createElement('div');
    loadingMessage.className = 'message bot-message';
    loadingMessage.textContent = 'Thinking...';
    chatContainer.appendChild(loadingMessage);

    // Scroll to loading message
    loadingMessage.scrollIntoView({ behavior: 'smooth' });

    // Send request to server
    fetch('/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: question })
    })
    .then(response => response.json())
    .then(data => {
        // Remove loading message
        chatContainer.removeChild(loadingMessage);
        
        // Create bot message container
        const botMessage = document.createElement('div');
        botMessage.className = 'message bot-message';
        chatContainer.appendChild(botMessage);

        // Progressive text rendering
        const words = data.response.split(' ');
        let currentIndex = 0;

        function addNextWord() {
            if (currentIndex < words.length) {
                const word = words[currentIndex];
                const span = document.createElement('span');
                span.className = 'typing-animation';
                span.textContent = word + ' ';
                botMessage.appendChild(span);
                
                // Scroll to the latest word
                span.scrollIntoView({ behavior: 'smooth', block: 'end' });
                
                currentIndex++;
                setTimeout(addNextWord, 50); // Adjust speed here
            }
        }

        addNextWord();
    })
    .catch(error => {
        // Remove loading message
        chatContainer.removeChild(loadingMessage);
        
        // Add error message
        const errorMessage = document.createElement('div');
        errorMessage.className = 'message bot-message';
        errorMessage.textContent = 'Sorry, there was an error processing your request.';
        chatContainer.appendChild(errorMessage);
        
        console.error('Error:', error);
    });
}

// Allow Enter key to send message
document.getElementById('userInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});