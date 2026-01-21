from flask import Blueprint, render_template, request
from flask_login import login_required
from app.models import Department

departments_bp = Blueprint('departments', __name__)

@departments_bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    departments = Department.query.paginate(page=page, per_page=10, error_out=False)
    return render_template('departments/index.html', departments=departments, title='Departments')
