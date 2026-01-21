from app import create_app

from app.models import User
from app.extensions import db

app = create_app('production')

# Vercel-specific: Auto-create tables and Admin user on cold start
# This ensures the DB is ready without manual shell commands
with app.app_context():
    try:
        db.create_all()
        
        # Ensure Admin User Exists
        if not User.query.filter_by(username='admin').first():
            print("Creating default admin user...")
            admin = User(username='admin', email='admin@school.com', role='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Admin user created.")
            
    except Exception as e:
        print(f"Database initialization error: {e}")
