from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import Department,db
from app.forms import DepartmentForm

departments_bp = Blueprint('departments', __name__)

@departments_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = DepartmentForm()
    if form.validate_on_submit():
        dept = Department(
            name=form.name.data,
            code=form.code.data,
            level=form.level.data,
            description=form.description.data
        )
        try:
            db.session.add(dept)
            db.session.commit()
            flash('Department added successfully!', 'success')
            return redirect(url_for('departments.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding department: {e}', 'error')
    return render_template('departments/add.html', form=form, title='Add Department')

@departments_bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    departments = Department.query.paginate(page=page, per_page=10, error_out=False)
    return render_template('departments/index.html', departments=departments, title='Departments')
