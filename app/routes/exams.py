from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import Exam, db
from app.forms import ExamForm

exams_bp = Blueprint('exams', __name__)

@exams_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = ExamForm()
    if form.validate_on_submit():
        exam = Exam(
            name=form.name.data,
            session=form.session.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data
        )
        try:
            db.session.add(exam)
            db.session.commit()
            flash('Exam scheduled successfully!', 'success')
            return redirect(url_for('exams.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error scheduling exam: {e}', 'error')
    return render_template('exams/add.html', form=form, title='Schedule Exam')

@exams_bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    exams = Exam.query.paginate(page=page, per_page=10, error_out=False)
    return render_template('exams/index.html', exams=exams, title='Exams')
