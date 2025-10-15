"""
AI Assistant Bot
Handles interactions with local LLM for document processing and user queries
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from backend.database.models import db, ActivityLog
from backend.config import Config
import os

ai_bp = Blueprint('ai', __name__)

# Check if LLM model exists
LLM_AVAILABLE = os.path.exists(Config.LLM_MODEL_PATH) if hasattr(Config, 'LLM_MODEL_PATH') else False

# Initialize LLM if available
llm = None
if LLM_AVAILABLE:
    try:
        from llama_cpp import Llama
        llm = Llama(
            model_path=Config.LLM_MODEL_PATH,
            n_ctx=Config.LLM_CONTEXT_SIZE,
            n_threads=4
        )
    except Exception as e:
        print(f"⚠️ Failed to load LLM model: {e}")
        LLM_AVAILABLE = False

@ai_bp.route('/api/ai/query', methods=['POST'])
@login_required
def query_ai():
    """Send a query to the AI assistant"""
    if not LLM_AVAILABLE:
        return jsonify({
            'error': 'AI assistant is not available. Please configure LLM model.',
            'mock_response': 'This is a mock response. Configure the LLM model to get real AI assistance.'
        }), 503
    
    data = request.get_json()
    if not data or not data.get('query'):
        return jsonify({'error': 'Query is required'}), 400
    
    query = data.get('query')
    context = data.get('context', '')
    
    try:
        # Build prompt
        prompt = f"""You are KoloCloud AI Assistant, helping military personnel with document management and queries.

Context: {context}

User Query: {query}

Assistant Response:"""
        
        # Generate response
        response = llm(
            prompt,
            max_tokens=512,
            temperature=Config.LLM_TEMPERATURE,
            stop=["User Query:", "\n\n"]
        )
        
        ai_response = response['choices'][0]['text'].strip()
        
        # Log activity
        log = ActivityLog(
            user_id=current_user.id,
            action='ai_query',
            details=f'AI query: {query[:100]}...',
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'query': query,
            'response': ai_response
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/api/ai/summarize', methods=['POST'])
@login_required
def summarize_document():
    """Summarize a document using AI"""
    if not LLM_AVAILABLE:
        return jsonify({
            'error': 'AI assistant is not available',
            'mock_response': 'This is a mock summary. Configure the LLM model for real summarization.'
        }), 503
    
    data = request.get_json()
    if not data or not data.get('text'):
        return jsonify({'error': 'Text is required'}), 400
    
    text = data.get('text')[:4000]  # Limit text length
    
    try:
        prompt = f"""Summarize the following document in Ukrainian:

{text}

Summary:"""
        
        response = llm(
            prompt,
            max_tokens=256,
            temperature=0.5,
            stop=["\n\nDocument:", "User:"]
        )
        
        summary = response['choices'][0]['text'].strip()
        
        # Log activity
        log = ActivityLog(
            user_id=current_user.id,
            action='ai_summarize',
            details='Document summarized by AI',
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'summary': summary
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/api/ai/status', methods=['GET'])
@login_required
def ai_status():
    """Get AI assistant status"""
    return jsonify({
        'available': LLM_AVAILABLE,
        'model_path': Config.LLM_MODEL_PATH if hasattr(Config, 'LLM_MODEL_PATH') else None,
        'message': 'AI assistant is ready' if LLM_AVAILABLE else 'AI assistant not configured'
    }), 200
