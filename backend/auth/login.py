"""
Authentication and Authorization
Handles user login, logout, JWT tokens, and session management
"""
from datetime import datetime
from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from backend.database.models import db, User, ActivityLog

auth_bp = Blueprint('auth', __name__)
login_manager = LoginManager()

def init_auth(app):
    """Initialize authentication system"""
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login_page'
    return login_manager

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    return User.query.get(int(user_id))

@auth_bp.route('/login', methods=['GET'])
def login_page():
    """Render login page"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('login.html')

@auth_bp.route('/api/login', methods=['POST'])
def login():
    """Handle user login"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Missing credentials'}), 400
    
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    
    if not user or not user.check_password(password):
        # Log failed attempt
        log = ActivityLog(
            action='login_failed',
            details=f'Failed login attempt for username: {username}',
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()
        return jsonify({'error': 'Invalid credentials'}), 401
    
    if not user.is_active:
        return jsonify({'error': 'Account is deactivated'}), 403
    
    # Login successful
    login_user(user, remember=data.get('remember', False))
    user.last_login = datetime.utcnow()
    
    # Log successful login
    log = ActivityLog(
        user_id=user.id,
        action='login_success',
        details=f'User {username} logged in',
        ip_address=request.remote_addr
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Login successful',
        'user': user.to_dict()
    }), 200

@auth_bp.route('/api/logout', methods=['POST'])
@login_required
def logout():
    """Handle user logout"""
    user_id = current_user.id
    username = current_user.username
    
    # Log logout
    log = ActivityLog(
        user_id=user_id,
        action='logout',
        details=f'User {username} logged out',
        ip_address=request.remote_addr
    )
    db.session.add(log)
    db.session.commit()
    
    logout_user()
    return jsonify({'success': True, 'message': 'Logout successful'}), 200

@auth_bp.route('/api/register', methods=['POST'])
def register():
    """Handle user registration"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password') or not data.get('email'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name', '')
    
    # Check if user already exists
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 409
    
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 409
    
    # Create new user
    user = User(
        username=username,
        email=email,
        full_name=full_name,
        role='user'
    )
    user.set_password(password)
    
    db.session.add(user)
    db.session.commit()
    
    # Log registration
    log = ActivityLog(
        user_id=user.id,
        action='user_registered',
        details=f'New user registered: {username}',
        ip_address=request.remote_addr
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Registration successful',
        'user': user.to_dict()
    }), 201

@auth_bp.route('/api/user/current', methods=['GET'])
@login_required
def current_user_info():
    """Get current user information"""
    return jsonify(current_user.to_dict()), 200

@auth_bp.route('/api/user/change-password', methods=['POST'])
@login_required
def change_password():
    """Change user password"""
    data = request.get_json()
    
    if not data or not data.get('old_password') or not data.get('new_password'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if not current_user.check_password(data.get('old_password')):
        return jsonify({'error': 'Invalid current password'}), 401
    
    current_user.set_password(data.get('new_password'))
    db.session.commit()
    
    # Log password change
    log = ActivityLog(
        user_id=current_user.id,
        action='password_changed',
        details=f'User {current_user.username} changed password',
        ip_address=request.remote_addr
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Password changed successfully'}), 200
