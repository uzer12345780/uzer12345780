"""
Logging Utility
Configures and manages application logging
"""
import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from rich.logging import RichHandler
from backend.config import Config, LOGS_DIR

def setup_logger(name: str = 'kolocloud', level: str = None) -> logging.Logger:
    """Setup application logger with file and console handlers"""
    
    if level is None:
        level = Config.LOG_LEVEL
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_formatter = logging.Formatter(
        '%(message)s',
        datefmt='%H:%M:%S'
    )
    
    # File handler with rotation
    log_file = Config.LOG_FILE
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)
    
    # Rich console handler for beautiful output
    console_handler = RichHandler(
        rich_tracebacks=True,
        markup=True,
        show_time=True,
        show_path=False
    )
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Create default logger
default_logger = setup_logger()

def log_info(message: str):
    """Log info message"""
    default_logger.info(message)

def log_warning(message: str):
    """Log warning message"""
    default_logger.warning(message)

def log_error(message: str):
    """Log error message"""
    default_logger.error(message)

def log_debug(message: str):
    """Log debug message"""
    default_logger.debug(message)

def log_critical(message: str):
    """Log critical message"""
    default_logger.critical(message)
