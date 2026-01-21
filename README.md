# School Management System

A comprehensive School and College Management System built with Flask and Tailwind CSS.

## Features
- **Student Management**: Enrolling, tracking academic records, etc.
- **Department Management**: Managing departments and faculties.
- **Fee Management**: Tracking payments, receipts, and outstanding dues.
- **Attendance**: Marking and viewing attendance.
- **Exams & Results**: Managing exams, marks, and report cards.
- **RBAC**: Role-based access control (Admin, Teacher, Student, etc.)

## Setup Instructions

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Initialize Database**:
    ```bash
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```

3.  **Create Admin User**:
    You can visit `/auth/create_admin` after running the app to create a default admin.
    Or run in python shell:
    ```python
    from app import db, create_app
    from app.models import User
    app = create_app()
    with app.app_context():
        u = User(username='admin', email='admin@school.com', role='admin')
        u.set_password('admin123')
        db.session.add(u)
        db.session.commit()
    ```

4.  **Run Application**:
    ```bash
    flask run
    # or
    python run.py
    ```

## Project Structure
- `app/`: Application source code.
- `app/models.py`: Database models.
- `app/routes/`: Route handlers (Controllers).
- `app/templates/`: HTML Templates.
- `config.py`: Configuration settings.
