from flask import Blueprint, render_template, request
from flask_login import login_required
from app.models import Exam

exams_bp = Blueprint('exams', __name__)

@exams_bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    exams = Exam.query.paginate(page=page, per_page=10, error_out=False)
    return render_template('exams/index.html', exams=exams, title='Exams')
