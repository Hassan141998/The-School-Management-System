from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Attendance, Student, db
from app.forms import AttendanceForm

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/mark', methods=['GET', 'POST'])
@login_required
def mark():
    form = AttendanceForm()
    form.student_id.choices = [(s.id, f"{s.reg_no} - {s.name}") for s in Student.query.all()]
    
    if form.validate_on_submit():
        att = Attendance(
            student_id=form.student_id.data,
            date=form.date.data,
            status=form.status.data,
            marked_by=current_user.username
        )
        try:
            db.session.add(att)
            db.session.commit()
            flash('Attendance marked successfully!', 'success')
            return redirect(url_for('attendance.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error marking attendance: {e}', 'error')
    return render_template('attendance/add.html', form=form, title='Mark Attendance')

@attendance_bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    attendance_records = Attendance.query.order_by(Attendance.date.desc()).paginate(page=page, per_page=15, error_out=False)
    return render_template('attendance/index.html', attendance_records=attendance_records, title='Attendance')
