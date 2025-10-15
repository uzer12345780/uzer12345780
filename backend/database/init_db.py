"""
Database Initialization
Creates tables and optionally seeds initial data
"""
from backend.database.models import db, User, File, ChatMessage, ActivityLog
from backend.config import Config

def init_database(app):
    """Initialize database with app context"""
    with app.app_context():
        db.init_app(app)
        db.create_all()
        print("✅ Database tables created successfully")
        
        # Create default admin user if not exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@kolocloud.local',
                full_name='System Administrator',
                role='admin'
            )
            admin.set_password('admin123')  # Change in production!
            db.session.add(admin)
            db.session.commit()
            print("✅ Default admin user created (username: admin, password: admin123)")
        
        return db

def reset_database(app):
    """Reset database - DROP ALL TABLES and recreate"""
    with app.app_context():
        db.drop_all()
        print("⚠️ All tables dropped")
        db.create_all()
        print("✅ Database reset successfully")
