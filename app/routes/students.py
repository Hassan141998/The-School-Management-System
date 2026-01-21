from flask import Blueprint, render_template, request
from flask_login import login_required
from app.models import Student

students_bp = Blueprint('students', __name__)

@students_bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    students = Student.query.paginate(page=page, per_page=10, error_out=False)
    return render_template('students/index.html', students=students, title='Students')
