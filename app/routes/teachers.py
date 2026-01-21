from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import Teacher, Department, db
from app.forms import TeacherForm

teachers_bp = Blueprint('teachers', __name__)

@teachers_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = TeacherForm()
    # Populate department choices
    form.department_id.choices = [(d.id, d.name) for d in Department.query.all()]
    
    if form.validate_on_submit():
        teacher = Teacher(
            employee_id=form.employee_id.data,
            name=form.name.data,
            email=form.email.data,
            contact=form.contact.data,
            designation=form.designation.data,
            department_id=form.department_id.data
        )
        try:
            db.session.add(teacher)
            db.session.commit()
            flash('Teacher added successfully!', 'success')
            return redirect(url_for('teachers.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding teacher: {e}', 'error')
    return render_template('teachers/add.html', form=form, title='Add Teacher')

@teachers_bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    teachers = Teacher.query.paginate(page=page, per_page=10, error_out=False)
    return render_template('teachers/index.html', teachers=teachers, title='Teachers')
