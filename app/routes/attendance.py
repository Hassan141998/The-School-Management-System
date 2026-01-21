from flask import Blueprint, render_template, request
from flask_login import login_required
from app.models import Attendance, Student

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    attendance_records = Attendance.query.order_by(Attendance.date.desc()).paginate(page=page, per_page=15, error_out=False)
    return render_template('attendance/index.html', attendance_records=attendance_records, title='Attendance')
