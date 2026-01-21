from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import Student, db
from app.forms import StudentForm

students_bp = Blueprint('students', __name__)

@students_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = StudentForm()
    if form.validate_on_submit():
        student = Student(
            reg_no=form.reg_no.data,
            name=form.name.data,
            father_name=form.father_name.data,
            email=form.email.data,
            contact=form.contact.data,
            dob=form.dob.data,
            gender=form.gender.data,
            address=form.address.data
        )
        try:
            db.session.add(student)
            db.session.commit()
            flash('Student added successfully!', 'success')
            return redirect(url_for('students.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding student: {e}', 'error')
    return render_template('students/add.html', form=form, title='Add Student')

@students_bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    students = Student.query.paginate(page=page, per_page=10, error_out=False)
    return render_template('students/index.html', students=students, title='Students')
