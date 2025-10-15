#!/usr/bin/env python3
"""
KoloCloud Structure Verification Script
Checks if all required files and directories are present
"""
import os
from pathlib import Path

def check_file(filepath, required=True):
    """Check if file exists"""
    exists = Path(filepath).exists()
    status = "✅" if exists else ("❌" if required else "⚠️")
    req_text = "" if required else " (optional)"
    print(f"{status} {filepath}{req_text}")
    return exists

def check_directory(dirpath, required=True):
    """Check if directory exists"""
    exists = Path(dirpath).is_dir()
    status = "✅" if exists else ("❌" if required else "⚠️")
    req_text = "" if required else " (optional)"
    print(f"{status} {dirpath}/{req_text}")
    return exists

def main():
    print("=" * 60)
    print("KoloCloud Project Structure Verification")
    print("=" * 60)
    
    missing_required = []
    
    print("\n📁 Backend Files:")
    files = [
        "backend/__init__.py",
        "backend/app.py",
        "backend/config.py",
        "backend/requirements.txt",
        "backend/database/__init__.py",
        "backend/database/models.py",
        "backend/database/init_db.py",
        "backend/auth/__init__.py",
        "backend/auth/login.py",
        "backend/files/__init__.py",
        "backend/files/handlers.py",
        "backend/ocr/__init__.py",
        "backend/ocr/ocr_engine.py",
        "backend/ai_assistant/__init__.py",
        "backend/ai_assistant/bot.py",
        "backend/ai_assistant/templates_gen.py",
        "backend/chat/__init__.py",
        "backend/chat/socketio_handler.py",
        "backend/utils/__init__.py",
        "backend/utils/security.py",
        "backend/utils/logger.py",
    ]
    
    for f in files:
        if not check_file(f):
            missing_required.append(f)
    
    print("\n🎨 Frontend Files:")
    frontend_files = [
        "frontend/templates/layout.html",
        "frontend/templates/login.html",
        "frontend/templates/dashboard.html",
        "frontend/templates/files.html",
        "frontend/templates/ocr_upload.html",
        "frontend/templates/bot.html",
        "frontend/templates/chat.html",
        "frontend/templates/admin.html",
        "frontend/static/css/main.css",
        "frontend/static/js/main.js",
        "frontend/static/js/chat.js",
    ]
    
    for f in frontend_files:
        if not check_file(f):
            missing_required.append(f)
    
    print("\n⚙️ Configuration Files:")
    config_files = [
        ("config/.env.example", True),
        ("config/settings.json", True),
        ("config/.env", False),
    ]
    
    for f, required in config_files:
        if not check_file(f, required) and required:
            missing_required.append(f)
    
    print("\n📂 Directories:")
    directories = [
        "data/users",
        "data/temp",
        "data/logs",
        "frontend/static/icons",
    ]
    
    for d in directories:
        if not check_directory(d):
            missing_required.append(d)
    
    print("\n🚀 Startup Scripts:")
    startup_files = [
        "start_server.sh",
        "start_server.bat",
    ]
    
    for f in startup_files:
        if not check_file(f):
            missing_required.append(f)
    
    print("\n📖 Documentation:")
    doc_files = [
        "README.md",
        "QUICKSTART.md",
    ]
    
    for f in doc_files:
        check_file(f)
    
    print("\n" + "=" * 60)
    
    if missing_required:
        print(f"❌ FAILED: {len(missing_required)} required files/directories missing:")
        for item in missing_required:
            print(f"   - {item}")
        print("\n⚠️  Please ensure all required files are present.")
        return False
    else:
        print("✅ SUCCESS: All required files and directories are present!")
        print("\n📌 Next steps:")
        print("   1. Review QUICKSTART.md for setup instructions")
        print("   2. Copy config/.env.example to config/.env")
        print("   3. Run ./start_server.sh (Linux/Mac) or start_server.bat (Windows)")
        print("   4. Access http://localhost:5000")
        print("   5. Login with admin/admin123")
        return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
