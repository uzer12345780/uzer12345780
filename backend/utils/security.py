"""
Security Utilities
Handles encryption, decryption, and hashing
"""
import os
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64

def generate_key_from_password(password: str, salt: bytes = None) -> tuple:
    """Generate encryption key from password"""
    if salt is None:
        salt = os.urandom(16)
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key, salt

def encrypt_data(data: bytes, key: str) -> bytes:
    """Encrypt data using Fernet symmetric encryption"""
    # Ensure key is in correct format
    if isinstance(key, str):
        if len(key) < 32:
            key = key.ljust(32, '!')[:32]
        key_bytes = key.encode()
    else:
        key_bytes = key
    
    encryption_key, _ = generate_key_from_password(key_bytes.decode())
    fernet = Fernet(encryption_key)
    
    encrypted_data = fernet.encrypt(data)
    return encrypted_data

def decrypt_data(encrypted_data: bytes, key: str) -> bytes:
    """Decrypt data using Fernet symmetric encryption"""
    # Ensure key is in correct format
    if isinstance(key, str):
        if len(key) < 32:
            key = key.ljust(32, '!')[:32]
        key_bytes = key.encode()
    else:
        key_bytes = key
    
    encryption_key, _ = generate_key_from_password(key_bytes.decode())
    fernet = Fernet(encryption_key)
    
    decrypted_data = fernet.decrypt(encrypted_data)
    return decrypted_data

def encrypt_file(filepath: str, key: str):
    """Encrypt a file in place"""
    with open(filepath, 'rb') as f:
        data = f.read()
    
    encrypted_data = encrypt_data(data, key)
    
    with open(filepath, 'wb') as f:
        f.write(encrypted_data)

def decrypt_file(input_filepath: str, output_filepath: str, key: str):
    """Decrypt a file to a new location"""
    with open(input_filepath, 'rb') as f:
        encrypted_data = f.read()
    
    decrypted_data = decrypt_data(encrypted_data, key)
    
    with open(output_filepath, 'wb') as f:
        f.write(decrypted_data)

def hash_text(text: str, algorithm='sha256') -> str:
    """Hash text using specified algorithm"""
    if algorithm == 'sha256':
        return hashlib.sha256(text.encode()).hexdigest()
    elif algorithm == 'sha512':
        return hashlib.sha512(text.encode()).hexdigest()
    elif algorithm == 'md5':
        return hashlib.md5(text.encode()).hexdigest()
    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")

def verify_hash(text: str, hash_value: str, algorithm='sha256') -> bool:
    """Verify text against hash"""
    return hash_text(text, algorithm) == hash_value

def generate_secure_token(length: int = 32) -> str:
    """Generate a secure random token"""
    return base64.urlsafe_b64encode(os.urandom(length)).decode()[:length]

def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent directory traversal"""
    # Remove path separators
    filename = filename.replace('/', '_').replace('\\', '_')
    # Remove any dangerous characters
    dangerous_chars = ['..', '<', '>', ':', '"', '|', '?', '*']
    for char in dangerous_chars:
        filename = filename.replace(char, '_')
    return filename
