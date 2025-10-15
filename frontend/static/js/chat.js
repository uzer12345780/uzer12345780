/**
 * KoloCloud Chat
 * Real-time chat functionality using Socket.IO
 */

let socket;
let currentRoom = 'general';
let typingTimeout;

// Initialize Socket.IO connection
function initializeChat() {
    socket = io({
        transports: ['websocket', 'polling']
    });
    
    // Connection events
    socket.on('connect', () => {
        console.log('✅ Connected to chat server');
        updateConnectionStatus(true);
        joinRoom(currentRoom);
    });
    
    socket.on('disconnect', () => {
        console.log('❌ Disconnected from chat server');
        updateConnectionStatus(false);
    });
    
    socket.on('connect_error', (error) => {
        console.error('Connection error:', error);
        updateConnectionStatus(false);
    });
    
    // Chat events
    socket.on('new_message', (data) => {
        addMessageToChat(data);
    });
    
    socket.on('user_connected', (data) => {
        showSystemMessage(`${data.username} приєднався до чату`);
        updateActiveUsers();
    });
    
    socket.on('user_disconnected', (data) => {
        showSystemMessage(`${data.username} покинув чат`);
        updateActiveUsers();
    });
    
    socket.on('active_users', (data) => {
        displayActiveUsers(data.users);
    });
    
    socket.on('user_typing', (data) => {
        showTypingIndicator(data);
    });
    
    socket.on('chat_history', (data) => {
        displayChatHistory(data.messages);
    });
    
    socket.on('message_deleted', (data) => {
        removeMessageFromChat(data.message_id);
    });
    
    socket.on('room_joined', (data) => {
        console.log('Joined room:', data.room);
    });
    
    socket.on('error', (data) => {
        showNotification(data.message, 'error');
    });
}

// Update connection status indicator
function updateConnectionStatus(isConnected) {
    const statusDiv = document.getElementById('connectionStatus');
    if (isConnected) {
        statusDiv.innerHTML = '<i class="fas fa-circle text-green-300"></i> З\'єднано';
    } else {
        statusDiv.innerHTML = '<i class="fas fa-circle text-red-300"></i> Відключено';
    }
}

// Join a chat room
function joinRoom(room) {
    if (socket && socket.connected) {
        socket.emit('join_room', { room });
        socket.emit('get_history', { room, limit: 50 });
    }
}

// Leave a room
function leaveRoom(room) {
    if (socket && socket.connected) {
        socket.emit('leave_room', { room });
    }
}

// Switch to a different room
function switchRoom(room) {
    leaveRoom(currentRoom);
    currentRoom = room;
    
    // Update UI
    document.getElementById('currentRoom').textContent = room;
    document.getElementById('messagesContainer').innerHTML = '';
    
    // Update room buttons
    document.querySelectorAll('.room-btn').forEach(btn => {
        btn.classList.remove('active', 'bg-green-50');
        btn.classList.add('bg-gray-50');
        
        if (btn.dataset.room === room) {
            btn.classList.add('active', 'bg-green-50');
            btn.classList.remove('bg-gray-50');
        }
    });
    
    joinRoom(room);
}

// Send message
function sendMessage(message) {
    if (!message.trim()) return;
    
    if (socket && socket.connected) {
        socket.emit('send_message', {
            message: message,
            room: currentRoom
        });
    } else {
        showNotification('Не вдається відправити повідомлення. Перевірте з\'єднання.', 'error');
    }
}

// Add message to chat
function addMessageToChat(data) {
    const container = document.getElementById('messagesContainer');
    
    // Remove welcome message if exists
    if (container.querySelector('.text-center')) {
        container.innerHTML = '';
    }
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'chat-message fade-in';
    messageDiv.dataset.messageId = data.id;
    
    const isCurrentUser = data.username === getCurrentUsername();
    
    messageDiv.innerHTML = `
        <div class="flex ${isCurrentUser ? 'justify-end' : 'justify-start'}">
            <div class="max-w-md">
                ${!isCurrentUser ? `<p class="text-xs text-gray-600 mb-1">${data.full_name || data.username}</p>` : ''}
                <div class="px-4 py-2 rounded-lg ${isCurrentUser ? 'bg-green-600 text-white' : 'bg-gray-200 text-gray-800'}">
                    <p>${escapeHtml(data.message)}</p>
                    <p class="text-xs mt-1 ${isCurrentUser ? 'text-green-100' : 'text-gray-600'}">
                        ${formatTime(data.timestamp)}
                    </p>
                </div>
            </div>
        </div>
    `;
    
    container.appendChild(messageDiv);
    container.scrollTop = container.scrollHeight;
}

// Show system message
function showSystemMessage(message) {
    const container = document.getElementById('messagesContainer');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'text-center text-sm text-gray-500 italic py-2 fade-in';
    messageDiv.textContent = message;
    container.appendChild(messageDiv);
}

// Display chat history
function displayChatHistory(messages) {
    const container = document.getElementById('messagesContainer');
    container.innerHTML = '';
    
    if (messages.length === 0) {
        container.innerHTML = `
            <div class="text-center text-gray-500 py-8">
                <i class="fas fa-comments text-6xl text-gray-300 mb-4"></i>
                <p>Поки що немає повідомлень у цій кімнаті</p>
            </div>
        `;
        return;
    }
    
    messages.forEach(msg => addMessageToChat(msg));
}

// Remove message from chat
function removeMessageFromChat(messageId) {
    const messageDiv = document.querySelector(`[data-message-id="${messageId}"]`);
    if (messageDiv) {
        messageDiv.style.opacity = '0';
        setTimeout(() => messageDiv.remove(), 300);
    }
}

// Display active users
function displayActiveUsers(users) {
    const container = document.getElementById('activeUsers');
    const count = document.getElementById('onlineCount');
    
    count.textContent = `(${users.length})`;
    
    if (users.length === 0) {
        container.innerHTML = '<p class="text-gray-500 text-sm">Немає активних користувачів</p>';
        return;
    }
    
    container.innerHTML = users.map(user => `
        <div class="flex items-center space-x-2 p-2 bg-green-50 rounded">
            <div class="status-online"></div>
            <span class="text-sm">${user.username}</span>
        </div>
    `).join('');
}

// Show typing indicator
function showTypingIndicator(data) {
    const indicator = document.getElementById('typingIndicator');
    
    if (data.typing && data.room === currentRoom) {
        indicator.textContent = `${data.username} набирає...`;
        indicator.classList.remove('hidden');
    } else {
        indicator.classList.add('hidden');
    }
}

// Emit typing event
function emitTyping(isTyping) {
    if (socket && socket.connected) {
        socket.emit('typing', {
            typing: isTyping,
            room: currentRoom
        });
    }
}

// Handle message form submission
document.getElementById('messageForm').addEventListener('submit', (e) => {
    e.preventDefault();
    
    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    
    if (message) {
        sendMessage(message);
        input.value = '';
        emitTyping(false);
    }
});

// Handle typing indicator
document.getElementById('messageInput').addEventListener('input', () => {
    clearTimeout(typingTimeout);
    emitTyping(true);
    
    typingTimeout = setTimeout(() => {
        emitTyping(false);
    }, 1000);
});

// Get current username (from page or storage)
function getCurrentUsername() {
    // Try to get from navigation bar
    const navUsername = document.querySelector('nav span i.fa-user')?.parentElement?.textContent?.trim();
    return navUsername || 'unknown';
}

// Format time
function formatTime(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('uk-UA', {
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Update active users periodically
function updateActiveUsers() {
    // The server will emit active_users event
}

// Initialize chat when page loads
document.addEventListener('DOMContentLoaded', () => {
    initializeChat();
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (socket && socket.connected) {
        leaveRoom(currentRoom);
        socket.disconnect();
    }
});
