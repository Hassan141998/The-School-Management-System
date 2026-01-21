from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    db.create_all()
    user = User.query.filter_by(username='admin').first()
    if user:
        print(f"Admin user found. Resetting password...")
        user.set_password('admin123')
        db.session.commit()
    else:
        print("Admin user not found. Creating...")
        user = User(username='admin', email='admin@school.com', role='admin')
        user.set_password('admin123')
        db.session.add(user)
        db.session.commit()
    
    print("Admin user ready: admin / admin123")
