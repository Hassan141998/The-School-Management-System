from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import FeePayment, Student, db
from app.forms import FeeForm
from datetime import datetime

fees_bp = Blueprint('fees', __name__)

@fees_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = FeeForm()
    form.student_id.choices = [(s.id, f"{s.reg_no} - {s.name}") for s in Student.query.all()]
    
    if form.validate_on_submit():
        payment = FeePayment(
            student_id=form.student_id.data,
            amount_paid=float(form.amount_paid.data),
            month=form.month.data,
            year=form.year.data,
            payment_method=form.payment_method.data,
            receipt_no=f"REC-{int(datetime.now().timestamp())}",
            received_by=current_user.username
        )
        try:
            db.session.add(payment)
            db.session.commit()
            flash('Fee collected successfully!', 'success')
            return redirect(url_for('fees.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error collecting fee: {e}', 'error')
    return render_template('fees/add.html', form=form, title='Collect Fee')

@fees_bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    payments = FeePayment.query.paginate(page=page, per_page=10, error_out=False)
    return render_template('fees/index.html', payments=payments, title='Fees')
