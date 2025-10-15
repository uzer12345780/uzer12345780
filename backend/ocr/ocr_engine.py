"""
OCR Engine
Handles text extraction from images using Tesseract
"""
import cv2
import pytesseract
from PIL import Image
from pathlib import Path
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from backend.database.models import db, File, ActivityLog
from backend.config import Config

ocr_bp = Blueprint('ocr', __name__)

# Configure Tesseract
pytesseract.pytesseract.tesseract_cmd = Config.TESSERACT_CMD

def preprocess_image(image_path):
    """Preprocess image for better OCR results"""
    # Read image
    img = cv2.imread(str(image_path))
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Denoise
    denoised = cv2.fastNlMeansDenoising(thresh, None, 10, 7, 21)
    
    return denoised

def extract_text_from_image(image_path, lang=None):
    """Extract text from image using OCR"""
    try:
        if lang is None:
            lang = Config.OCR_LANGUAGES
        
        # Preprocess image
        processed_img = preprocess_image(image_path)
        
        # Perform OCR
        text = pytesseract.image_to_string(processed_img, lang=lang)
        
        return text.strip()
    except Exception as e:
        raise Exception(f"OCR failed: {str(e)}")

@ocr_bp.route('/api/ocr/process/<int:file_id>', methods=['POST'])
@login_required
def process_file_ocr(file_id):
    """Process OCR on an uploaded file"""
    file = File.query.filter_by(id=file_id, user_id=current_user.id).first()
    
    if not file:
        return jsonify({'error': 'File not found'}), 404
    
    # Check if file is an image
    if file.file_type not in ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff']:
        return jsonify({'error': 'File is not an image'}), 400
    
    filepath = Path(file.filepath)
    if not filepath.exists():
        return jsonify({'error': 'File not found on disk'}), 404
    
    try:
        # Extract text
        lang = request.json.get('language', Config.OCR_LANGUAGES) if request.json else Config.OCR_LANGUAGES
        text = extract_text_from_image(str(filepath), lang)
        
        # Save OCR text to database
        file.ocr_text = text
        db.session.commit()
        
        # Log activity
        log = ActivityLog(
            user_id=current_user.id,
            action='ocr_processed',
            details=f'OCR processed for file: {file.original_filename}',
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'text': text,
            'file_id': file.id
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ocr_bp.route('/api/ocr/upload-and-process', methods=['POST'])
@login_required
def upload_and_process():
    """Upload image and immediately process OCR"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Check if file is an image
    file_extension = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
    if file_extension not in ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff']:
        return jsonify({'error': 'File must be an image'}), 400
    
    try:
        # Save temporarily
        from werkzeug.utils import secure_filename
        import uuid
        from backend.config import TEMP_DIR
        
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        temp_path = TEMP_DIR / unique_filename
        file.save(str(temp_path))
        
        # Extract text
        lang = request.form.get('language', Config.OCR_LANGUAGES)
        text = extract_text_from_image(str(temp_path), lang)
        
        # Optionally save to user's files
        save_file = request.form.get('save', 'false').lower() == 'true'
        
        if save_file:
            from backend.files.handlers import get_user_directory
            
            user_dir = get_user_directory(current_user.id)
            final_path = user_dir / unique_filename
            temp_path.rename(final_path)
            
            # Create database record
            file_record = File(
                filename=unique_filename,
                original_filename=filename,
                filepath=str(final_path),
                file_type=file_extension,
                file_size=final_path.stat().st_size,
                is_encrypted=False,
                ocr_text=text,
                user_id=current_user.id
            )
            db.session.add(file_record)
            db.session.commit()
            
            file_id = file_record.id
        else:
            # Clean up temp file
            if temp_path.exists():
                temp_path.unlink()
            file_id = None
        
        # Log activity
        log = ActivityLog(
            user_id=current_user.id,
            action='ocr_processed',
            details=f'OCR processed for uploaded image: {filename}',
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'text': text,
            'file_id': file_id,
            'saved': save_file
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
