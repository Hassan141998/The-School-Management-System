from flask import Flask
from config import config
from app.extensions import db, login_manager, migrate, mail, csrf

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    csrf.init_app(app)

    # Login manager configuration
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # Register blueprints
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.routes.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp)

    from app.routes.students import students_bp
    app.register_blueprint(students_bp, url_prefix='/students')

    from app.routes.teachers import teachers_bp
    app.register_blueprint(teachers_bp, url_prefix='/teachers')

    from app.routes.departments import departments_bp
    app.register_blueprint(departments_bp, url_prefix='/departments')

    from app.routes.fees import fees_bp
    app.register_blueprint(fees_bp, url_prefix='/fees')

    from app.routes.attendance import attendance_bp
    app.register_blueprint(attendance_bp, url_prefix='/attendance')

    from app.routes.exams import exams_bp
    app.register_blueprint(exams_bp, url_prefix='/exams')

    from app.routes.settings import settings_bp
    app.register_blueprint(settings_bp, url_prefix='/settings')

    return app
