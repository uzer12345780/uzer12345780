"""
KoloCloud Configuration
Manages application settings, paths, and security keys
"""
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / 'data'
USERS_DIR = DATA_DIR / 'users'
TEMP_DIR = DATA_DIR / 'temp'
LOGS_DIR = DATA_DIR / 'logs'

# Ensure directories exist
for directory in [DATA_DIR, USERS_DIR, TEMP_DIR, LOGS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Flask configuration
class Config:
    # Secret key for sessions
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI', 
        f'sqlite:///{DATA_DIR}/kolocloud.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File upload configuration
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB max file size
    UPLOAD_FOLDER = TEMP_DIR
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xls', 'xlsx'}
    
    # Session configuration
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    
    # Security configuration
    ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY', 'default-encryption-key-32bytes!')
    PASSWORD_SALT = os.getenv('PASSWORD_SALT', b'kolocloud-salt')
    
    # OCR configuration
    TESSERACT_CMD = os.getenv('TESSERACT_CMD', '/usr/bin/tesseract')
    OCR_LANGUAGES = 'ukr+eng'  # Ukrainian and English
    
    # AI Assistant configuration
    LLM_MODEL_PATH = os.getenv('LLM_MODEL_PATH', './models/llama-model.gguf')
    LLM_CONTEXT_SIZE = 2048
    LLM_TEMPERATURE = 0.7
    
    # SocketIO configuration
    SOCKETIO_ASYNC_MODE = 'eventlet'
    
    # Logging configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = LOGS_DIR / 'kolocloud.log'
