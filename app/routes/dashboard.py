from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Student, Teacher, FeePayment, Department

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
@login_required
def index():
    # Placeholder data needed for dashboard
    stats = {
        'total_students': Student.query.count(),
        'total_teachers': Teacher.query.count(),
        'active_departments': Department.query.count(),
        # Pending fees logic would go here, simplistic placeholder for now
        'pending_fees': 125000 
    }
    
    # Recent activities (mockup)
    recent_activities = [
        {'title': 'Fee Payment Received', 'desc': 'Student John Doe paid $500', 'time': '2 hours ago', 'icon': 'fa-money-bill-wave', 'color': 'text-green-500'},
        {'title': 'New Admission', 'desc': 'Sarah Smith joined Class 10', 'time': '5 hours ago', 'icon': 'fa-user-plus', 'color': 'text-blue-500'},
        {'title': 'Attendance Alert', 'desc': 'Class 9B attendance marked', 'time': '1 day ago', 'icon': 'fa-calendar-check', 'color': 'text-purple-500'},
    ]
    
    return render_template('dashboard.html', title='Dashboard', stats=stats, recent_activities=recent_activities)
