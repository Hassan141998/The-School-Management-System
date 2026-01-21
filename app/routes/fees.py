from flask import Blueprint, render_template, request
from flask_login import login_required
from app.models import FeePayment

fees_bp = Blueprint('fees', __name__)

@fees_bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    payments = FeePayment.query.paginate(page=page, per_page=10, error_out=False)
    return render_template('fees/index.html', payments=payments, title='Fees')
