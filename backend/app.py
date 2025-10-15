"""
KoloCloud - Military Cloud Storage System
Main Flask Application Server
"""
from flask import Flask, render_template, redirect, url_for
from flask_cors import CORS
from flask_login import login_required, current_user
from backend.config import Config
from backend.database.models import db
from backend.database.init_db import init_database
from backend.auth.login import auth_bp, init_auth
from backend.files.handlers import files_bp
from backend.ocr.ocr_engine import ocr_bp
from backend.ai_assistant.bot import ai_bp
from backend.ai_assistant.templates_gen import templates_bp
from backend.chat.socketio_handler import init_socketio
from backend.utils.logger import setup_logger
import os

# Setup logger
logger = setup_logger('kolocloud')

def create_app(config_class=Config):
    """Application factory"""
    app = Flask(__name__, 
                template_folder='../frontend/templates',
                static_folder='../frontend/static')
    
    # Load configuration
    app.config.from_object(config_class)
    
    # Initialize extensions
    CORS(app)
    
    # Initialize database
    init_database(app)
    
    # Initialize authentication
    init_auth(app)
    
    # Initialize SocketIO for chat
    socketio = init_socketio(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(files_bp)
    app.register_blueprint(ocr_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(templates_bp)
    
    # Main routes
    @app.route('/')
    def index():
        """Home page"""
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        return redirect(url_for('auth.login_page'))
    
    @app.route('/dashboard')
    @login_required
    def dashboard():
        """User dashboard"""
        return render_template('dashboard.html', user=current_user)
    
    @app.route('/files')
    @login_required
    def files_page():
        """File manager page"""
        return render_template('files.html', user=current_user)
    
    @app.route('/ocr')
    @login_required
    def ocr_page():
        """OCR upload page"""
        return render_template('ocr_upload.html', user=current_user)
    
    @app.route('/bot')
    @login_required
    def bot_page():
        """AI assistant page"""
        return render_template('bot.html', user=current_user)
    
    @app.route('/chat')
    @login_required
    def chat_page():
        """Chat page"""
        return render_template('chat.html', user=current_user)
    
    @app.route('/admin')
    @login_required
    def admin_page():
        """Admin panel"""
        if current_user.role != 'admin':
            return redirect(url_for('dashboard'))
        return render_template('admin.html', user=current_user)
    
    @app.route('/health')
    def health_check():
        """Health check endpoint"""
        return {'status': 'healthy', 'service': 'KoloCloud'}, 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return render_template('login.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        logger.error(f"Internal error: {error}")
        return {'error': 'Internal server error'}, 500
    
    logger.info("🚀 KoloCloud application initialized")
    
    return app, socketio

if __name__ == '__main__':
    app, socketio = create_app()
    
    # Run with SocketIO
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"🌐 Starting KoloCloud server on {host}:{port}")
    logger.info(f"🔐 Debug mode: {debug}")
    
    socketio.run(app, host=host, port=port, debug=debug, allow_unsafe_werkzeug=True)
