document.addEventListener('DOMContentLoaded', () => {
  const chatForm = document.getElementById('chat-form');
  const chatInput = document.getElementById('chat-input');
  const chatMessages = document.getElementById('chat-messages');
  const sessionIdDisplay = document.getElementById('session-id-display');
  const copySessionBtn = document.getElementById('copy-session-btn');
  const existingSessionInput = document.getElementById('existing-session-input');
  const loadSessionBtn = document.getElementById('load-session-btn');
  const newChatBtn = document.getElementById('new-chat-btn');

  let currentSessionId = localStorage.getItem('adk_session_id') || null;

  // Initialize UI
  updateSessionUI();

  // Auto-resize textarea
  chatInput.addEventListener('input', () => {
    chatInput.style.height = 'auto';
    chatInput.style.height = (chatInput.scrollHeight - 16) + 'px';
  });

  // Handle send message
  chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const query = chatInput.value.trim();
    if (!query) return;

    // Reset input box height
    chatInput.value = '';
    chatInput.style.height = 'auto';

    // Append User message
    appendMessage('user', 'You', query);

    // Append typing indicator
    const typingIndicator = appendTypingIndicator();
    chatMessages.scrollTop = chatMessages.scrollHeight;

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          query: query,
          session_id: currentSessionId
        })
      });

      // Remove typing indicator
      typingIndicator.remove();

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.error || 'Failed to get response');
      }

      const data = await response.json();
      if (data.status === 'success' && data.results) {
        const { session_id, response: responseText } = data.results;
        
        // Update session ID if it changed or was newly created
        if (session_id && session_id !== currentSessionId) {
          currentSessionId = session_id;
          localStorage.setItem('adk_session_id', session_id);
          updateSessionUI();
        }

        // Append Agent response
        appendMessage('agent', 'Root Agent', responseText);
      } else {
        throw new Error('Unexpected response format');
      }

    } catch (err) {
      console.error(err);
      appendMessage('agent', 'System Error', `Error: ${err.message}. Please check if the FastAPI server is running on port 8000.`);
    }

    chatMessages.scrollTop = chatMessages.scrollHeight;
  });

  // Load existing session
  loadSessionBtn.addEventListener('click', () => {
    const targetSessionId = existingSessionInput.value.trim();
    if (!targetSessionId) return;

    currentSessionId = targetSessionId;
    localStorage.setItem('adk_session_id', currentSessionId);
    updateSessionUI();
    existingSessionInput.value = '';
    
    // Add system notification in chat
    appendSystemMessage(`Session loaded: ${currentSessionId}`);
  });

  // Start new session
  newChatBtn.addEventListener('click', () => {
    currentSessionId = null;
    localStorage.removeItem('adk_session_id');
    updateSessionUI();
    
    // Clear message history & reset with system welcome message
    chatMessages.innerHTML = `
      <div class="system-message">
        <p>New session initialized. A new Session ID will be generated upon sending your first message.</p>
      </div>
    `;
  });

  // Copy Session ID to clipboard
  copySessionBtn.addEventListener('click', () => {
    if (!currentSessionId) return;
    navigator.clipboard.writeText(currentSessionId).then(() => {
      const originalSvg = copySessionBtn.innerHTML;
      // Show checkmark
      copySessionBtn.innerHTML = `
        <svg width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="#10B981" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
        </svg>
      `;
      setTimeout(() => {
        copySessionBtn.innerHTML = originalSvg;
      }, 2000);
    });
  });

  // UI Helper Functions
  function updateSessionUI() {
    if (currentSessionId) {
      sessionIdDisplay.textContent = currentSessionId;
      copySessionBtn.removeAttribute('disabled');
    } else {
      sessionIdDisplay.textContent = 'None (Will auto-generate)';
      copySessionBtn.setAttribute('disabled', 'true');
    }
  }

  function appendMessage(senderType, senderName, text) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', senderType);

    const senderSpan = document.createElement('span');
    senderSpan.classList.add('message-sender');
    senderSpan.textContent = senderName;

    const bubbleDiv = document.createElement('div');
    bubbleDiv.classList.add('message-bubble');
    // Simple line break support
    bubbleDiv.innerHTML = text.replace(/\n/g, '<br>');

    const timeDiv = document.createElement('div');
    timeDiv.classList.add('message-time');
    const now = new Date();
    timeDiv.textContent = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    messageDiv.appendChild(senderSpan);
    messageDiv.appendChild(bubbleDiv);
    messageDiv.appendChild(timeDiv);

    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function appendSystemMessage(text) {
    const systemDiv = document.createElement('div');
    systemDiv.classList.add('system-message');
    systemDiv.innerHTML = `<p>${text}</p>`;
    chatMessages.appendChild(systemDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function appendTypingIndicator() {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', 'agent');

    const senderSpan = document.createElement('span');
    senderSpan.classList.add('message-sender');
    senderSpan.textContent = 'Root Agent';

    const bubbleDiv = document.createElement('div');
    bubbleDiv.classList.add('message-bubble');

    const indicator = document.createElement('div');
    indicator.classList.add('typing-indicator');
    indicator.innerHTML = `
      <div class="typing-dot"></div>
      <div class="typing-dot"></div>
      <div class="typing-dot"></div>
    `;

    bubbleDiv.appendChild(indicator);
    messageDiv.appendChild(senderSpan);
    messageDiv.appendChild(bubbleDiv);
    chatMessages.appendChild(messageDiv);
    return messageDiv;
  }
});
