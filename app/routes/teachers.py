from flask import Blueprint, render_template, request
from flask_login import login_required
from app.models import Teacher

teachers_bp = Blueprint('teachers', __name__)

@teachers_bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    teachers = Teacher.query.paginate(page=page, per_page=10, error_out=False)
    return render_template('teachers/index.html', teachers=teachers, title='Teachers')
