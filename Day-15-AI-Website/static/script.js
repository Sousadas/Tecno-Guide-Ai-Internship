document.addEventListener('DOMContentLoaded', () => {
    const chatToggleBtn = document.getElementById('chat-toggle');
    const chatWindow = document.getElementById('chat-window');
    const closeChatBtn = document.getElementById('close-chat');
    const iconOpen = document.getElementById('chat-icon-open');
    const iconClose = document.getElementById('chat-icon-close');
    
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages');
    const sendBtn = document.getElementById('send-btn');
    const typingIndicator = document.getElementById('typing-indicator');

    let isChatOpen = false;

    // Toggle Chat Window
    function toggleChat() {
        isChatOpen = !isChatOpen;
        
        if (isChatOpen) {
            chatWindow.classList.remove('hidden');
            // Small delay to allow display:block to apply before transition
            setTimeout(() => {
                chatWindow.classList.add('chat-window-open');
            }, 10);

            // Animate Icon
            iconOpen.classList.replace('scale-100', 'scale-0');
            iconOpen.classList.replace('opacity-100', 'opacity-0');
            iconOpen.classList.replace('rotate-0', 'rotate-90');
            
            iconClose.classList.replace('scale-0', 'scale-100');
            iconClose.classList.replace('opacity-0', 'opacity-100');
            iconClose.classList.replace('-rotate-90', 'rotate-0');
            
            // Focus input
            setTimeout(() => chatInput.focus(), 300);
        } else {
            chatWindow.classList.remove('chat-window-open');
            setTimeout(() => {
                chatWindow.classList.add('hidden');
            }, 300); // Wait for transition

            // Animate Icon back
            iconOpen.classList.replace('scale-0', 'scale-100');
            iconOpen.classList.replace('opacity-0', 'opacity-100');
            iconOpen.classList.replace('rotate-90', 'rotate-0');
            
            iconClose.classList.replace('scale-100', 'scale-0');
            iconClose.classList.replace('opacity-100', 'opacity-0');
            iconClose.classList.replace('rotate-0', '-rotate-90');
        }
    }

    chatToggleBtn.addEventListener('click', toggleChat);
    closeChatBtn.addEventListener('click', toggleChat);

    // Simple markdown to HTML parser for basic formatting (bold, code, lists)
    function parseMarkdown(text) {
        let html = text
            // Code blocks
            .replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>')
            // Inline code
            .replace(/`([^`]+)`/g, '<code>$1</code>')
            // Bold
            .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
            // Newlines to br (if not inside pre/ul/ol) - simplified
            .replace(/\n\n/g, '</p><p>')
            .replace(/\n/g, '<br>');
        
        // Basic list support (very naive, just for display)
        html = html.replace(/(?:^|<br>)\* (.*?)(?=(?:<br>|$))/g, '<ul><li>$1</li></ul>');
        // Clean up adjacent uls
        html = html.replace(/<\/ul><ul>/g, '');

        return `<div class="markdown-body"><p>${html}</p></div>`;
    }

    // Add Message to Chat UI
    function appendMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('flex', 'items-start', 'gap-2.5', 'message-animate');

        if (sender === 'user') {
            messageDiv.classList.add('justify-end', 'pl-10');
            messageDiv.innerHTML = `
                <div class="bg-indigo-600 border border-indigo-700 shadow-sm p-3 text-sm text-white rounded-2xl rounded-tr-none max-w-[85%] leading-relaxed whitespace-pre-wrap">
                    ${text.replace(/</g, "&lt;").replace(/>/g, "&gt;")}
                </div>
            `;
        } else {
            messageDiv.classList.add('pr-10');
            const htmlContent = parseMarkdown(text);
            messageDiv.innerHTML = `
                <div class="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-500 to-purple-500 flex-shrink-0 flex items-center justify-center text-white shadow-sm mt-0.5">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg>
                </div>
                <div class="bg-white border border-gray-100 shadow-sm p-3 text-sm text-gray-800 rounded-2xl rounded-tl-none max-w-[85%] leading-relaxed">
                    ${htmlContent}
                </div>
            `;
        }

        chatMessages.appendChild(messageDiv);
        scrollToBottom();
    }

    function scrollToBottom() {
        chatMessages.scrollTo({
            top: chatMessages.scrollHeight,
            behavior: 'smooth'
        });
    }

    // Handle Form Submission
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const message = chatInput.value.trim();
        if (!message) return;

        // Display user message
        appendMessage(message, 'user');
        chatInput.value = '';
        chatInput.focus();

        // Show typing indicator
        typingIndicator.classList.remove('hidden');
        scrollToBottom();

        // Disable input while waiting
        chatInput.disabled = true;
        sendBtn.disabled = true;
        sendBtn.classList.add('opacity-50');

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message })
            });

            const data = await response.json();

            // Hide typing indicator
            typingIndicator.classList.add('hidden');

            if (response.ok) {
                appendMessage(data.reply, 'bot');
            } else {
                appendMessage(`Error: ${data.error || 'Something went wrong.'}`, 'bot');
            }
        } catch (error) {
            typingIndicator.classList.add('hidden');
            appendMessage('Network error: Could not reach the server.', 'bot');
            console.error('Error calling /api/chat:', error);
        } finally {
            // Re-enable input
            chatInput.disabled = false;
            sendBtn.disabled = false;
            sendBtn.classList.remove('opacity-50');
            chatInput.focus();
        }
    });
});
