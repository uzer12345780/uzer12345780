"""
Real-time Chat Handler
Manages WebSocket connections for real-time chat using SocketIO
"""
from flask import request
from flask_socketio import SocketIO, emit, join_room, leave_room, rooms
from flask_login import current_user
from backend.database.models import db, ChatMessage, User
from datetime import datetime

socketio = SocketIO()

def init_socketio(app):
    """Initialize SocketIO with Flask app"""
    socketio.init_app(app, cors_allowed_origins="*", async_mode='eventlet')
    return socketio

# Store active users
active_users = {}

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    if current_user.is_authenticated:
        user_id = current_user.id
        username = current_user.username
        active_users[request.sid] = {
            'user_id': user_id,
            'username': username
        }
        
        # Notify others
        emit('user_connected', {
            'user_id': user_id,
            'username': username,
            'timestamp': datetime.utcnow().isoformat()
        }, broadcast=True, include_self=False)
        
        # Send active users list to the connected user
        emit('active_users', {
            'users': list(active_users.values())
        })
        
        print(f"✅ User {username} connected")

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    if request.sid in active_users:
        user_info = active_users.pop(request.sid)
        
        # Notify others
        emit('user_disconnected', {
            'user_id': user_info['user_id'],
            'username': user_info['username'],
            'timestamp': datetime.utcnow().isoformat()
        }, broadcast=True)
        
        print(f"❌ User {user_info['username']} disconnected")

@socketio.on('join_room')
def handle_join_room(data):
    """Handle user joining a chat room"""
    room = data.get('room', 'general')
    join_room(room)
    
    if current_user.is_authenticated:
        emit('room_joined', {
            'room': room,
            'username': current_user.username,
            'timestamp': datetime.utcnow().isoformat()
        }, room=room)
        
        print(f"User {current_user.username} joined room: {room}")

@socketio.on('leave_room')
def handle_leave_room(data):
    """Handle user leaving a chat room"""
    room = data.get('room', 'general')
    leave_room(room)
    
    if current_user.is_authenticated:
        emit('room_left', {
            'room': room,
            'username': current_user.username,
            'timestamp': datetime.utcnow().isoformat()
        }, room=room)
        
        print(f"User {current_user.username} left room: {room}")

@socketio.on('send_message')
def handle_send_message(data):
    """Handle sending a chat message"""
    if not current_user.is_authenticated:
        emit('error', {'message': 'Not authenticated'})
        return
    
    message_text = data.get('message', '').strip()
    room = data.get('room', 'general')
    
    if not message_text:
        emit('error', {'message': 'Empty message'})
        return
    
    # Save message to database
    message = ChatMessage(
        user_id=current_user.id,
        message=message_text,
        room=room
    )
    db.session.add(message)
    db.session.commit()
    
    # Broadcast message to room
    emit('new_message', {
        'id': message.id,
        'user_id': current_user.id,
        'username': current_user.username,
        'full_name': current_user.full_name,
        'message': message_text,
        'room': room,
        'timestamp': message.created_at.isoformat()
    }, room=room)
    
    print(f"Message from {current_user.username} in {room}: {message_text[:50]}...")

@socketio.on('typing')
def handle_typing(data):
    """Handle typing indicator"""
    if not current_user.is_authenticated:
        return
    
    room = data.get('room', 'general')
    is_typing = data.get('typing', False)
    
    emit('user_typing', {
        'user_id': current_user.id,
        'username': current_user.username,
        'typing': is_typing,
        'room': room
    }, room=room, include_self=False)

@socketio.on('get_history')
def handle_get_history(data):
    """Get chat history for a room"""
    if not current_user.is_authenticated:
        emit('error', {'message': 'Not authenticated'})
        return
    
    room = data.get('room', 'general')
    limit = data.get('limit', 50)
    
    # Fetch messages from database
    messages = ChatMessage.query.filter_by(room=room)\
        .order_by(ChatMessage.created_at.desc())\
        .limit(limit)\
        .all()
    
    messages.reverse()  # Show oldest first
    
    emit('chat_history', {
        'room': room,
        'messages': [msg.to_dict() for msg in messages]
    })

@socketio.on('delete_message')
def handle_delete_message(data):
    """Delete a message (only by author or admin)"""
    if not current_user.is_authenticated:
        emit('error', {'message': 'Not authenticated'})
        return
    
    message_id = data.get('message_id')
    if not message_id:
        emit('error', {'message': 'Message ID required'})
        return
    
    message = ChatMessage.query.get(message_id)
    
    if not message:
        emit('error', {'message': 'Message not found'})
        return
    
    # Check permissions
    if message.user_id != current_user.id and current_user.role != 'admin':
        emit('error', {'message': 'Permission denied'})
        return
    
    room = message.room
    db.session.delete(message)
    db.session.commit()
    
    # Notify room about deleted message
    emit('message_deleted', {
        'message_id': message_id,
        'room': room
    }, room=room)
