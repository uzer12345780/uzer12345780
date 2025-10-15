"""
File Management Handlers
Handles file upload, download, deletion, and browsing
"""
import os
import uuid
from datetime import datetime
from pathlib import Path
from flask import Blueprint, request, jsonify, send_file
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from backend.database.models import db, File, ActivityLog
from backend.config import Config, USERS_DIR
from backend.utils.security import encrypt_file, decrypt_file

files_bp = Blueprint('files', __name__)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def get_user_directory(user_id):
    """Get or create user's file directory"""
    user_dir = USERS_DIR / str(user_id)
    user_dir.mkdir(parents=True, exist_ok=True)
    return user_dir

@files_bp.route('/api/files/upload', methods=['POST'])
@login_required
def upload_file():
    """Upload a file"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400
    
    # Secure filename and create unique name
    original_filename = secure_filename(file.filename)
    file_extension = original_filename.rsplit('.', 1)[1].lower()
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    
    # Get user directory
    user_dir = get_user_directory(current_user.id)
    filepath = user_dir / unique_filename
    
    # Save file
    file.save(str(filepath))
    file_size = filepath.stat().st_size
    
    # Check if encryption is requested
    encrypt = request.form.get('encrypt', 'false').lower() == 'true'
    if encrypt:
        encrypt_file(str(filepath), Config.ENCRYPTION_KEY)
    
    # Create database record
    file_record = File(
        filename=unique_filename,
        original_filename=original_filename,
        filepath=str(filepath),
        file_type=file_extension,
        file_size=file_size,
        is_encrypted=encrypt,
        user_id=current_user.id,
        tags=request.form.get('tags', '')
    )
    
    db.session.add(file_record)
    
    # Log activity
    log = ActivityLog(
        user_id=current_user.id,
        action='file_uploaded',
        details=f'Uploaded file: {original_filename}',
        ip_address=request.remote_addr
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'File uploaded successfully',
        'file': file_record.to_dict()
    }), 201

@files_bp.route('/api/files', methods=['GET'])
@login_required
def list_files():
    """List all files for current user"""
    files = File.query.filter_by(user_id=current_user.id).order_by(File.uploaded_at.desc()).all()
    
    return jsonify({
        'files': [f.to_dict() for f in files],
        'count': len(files)
    }), 200

@files_bp.route('/api/files/<int:file_id>', methods=['GET'])
@login_required
def get_file_info(file_id):
    """Get file information"""
    file = File.query.filter_by(id=file_id, user_id=current_user.id).first()
    
    if not file:
        return jsonify({'error': 'File not found'}), 404
    
    return jsonify(file.to_dict()), 200

@files_bp.route('/api/files/<int:file_id>/download', methods=['GET'])
@login_required
def download_file(file_id):
    """Download a file"""
    file = File.query.filter_by(id=file_id, user_id=current_user.id).first()
    
    if not file:
        return jsonify({'error': 'File not found'}), 404
    
    filepath = Path(file.filepath)
    if not filepath.exists():
        return jsonify({'error': 'File not found on disk'}), 404
    
    # If file is encrypted, decrypt it temporarily
    if file.is_encrypted:
        temp_path = filepath.parent / f"temp_{filepath.name}"
        decrypt_file(str(filepath), str(temp_path), Config.ENCRYPTION_KEY)
        
        # Log activity
        log = ActivityLog(
            user_id=current_user.id,
            action='file_downloaded',
            details=f'Downloaded file: {file.original_filename}',
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()
        
        response = send_file(
            str(temp_path),
            as_attachment=True,
            download_name=file.original_filename
        )
        
        # Clean up temp file after sending
        @response.call_on_close
        def cleanup():
            if temp_path.exists():
                temp_path.unlink()
        
        return response
    else:
        # Log activity
        log = ActivityLog(
            user_id=current_user.id,
            action='file_downloaded',
            details=f'Downloaded file: {file.original_filename}',
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()
        
        return send_file(
            str(filepath),
            as_attachment=True,
            download_name=file.original_filename
        )

@files_bp.route('/api/files/<int:file_id>', methods=['DELETE'])
@login_required
def delete_file(file_id):
    """Delete a file"""
    file = File.query.filter_by(id=file_id, user_id=current_user.id).first()
    
    if not file:
        return jsonify({'error': 'File not found'}), 404
    
    # Delete file from disk
    filepath = Path(file.filepath)
    if filepath.exists():
        filepath.unlink()
    
    # Delete database record
    db.session.delete(file)
    
    # Log activity
    log = ActivityLog(
        user_id=current_user.id,
        action='file_deleted',
        details=f'Deleted file: {file.original_filename}',
        ip_address=request.remote_addr
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'File deleted successfully'}), 200

@files_bp.route('/api/files/search', methods=['GET'])
@login_required
def search_files():
    """Search files by name or tags"""
    query = request.args.get('q', '')
    
    if not query:
        return jsonify({'files': [], 'count': 0}), 200
    
    # Search in filename and tags
    files = File.query.filter(
        File.user_id == current_user.id,
        db.or_(
            File.original_filename.contains(query),
            File.tags.contains(query),
            File.ocr_text.contains(query)
        )
    ).order_by(File.uploaded_at.desc()).all()
    
    return jsonify({
        'files': [f.to_dict() for f in files],
        'count': len(files),
        'query': query
    }), 200
