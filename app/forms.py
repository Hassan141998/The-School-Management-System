from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class StudentForm(FlaskForm):
    reg_no = StringField('Registration No', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    father_name = StringField('Father Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    contact = StringField('Contact')
    dob = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female')], validators=[DataRequired()])
    address = StringField('Address')
    submit = SubmitField('Add Student')

class TeacherForm(FlaskForm):
    employee_id = StringField('Employee ID', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    contact = StringField('Contact')
    designation = StringField('Designation', validators=[DataRequired()])
    department_id = SelectField('Department', coerce=int, validators=[DataRequired()])
    department_id = SelectField('Department', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add Teacher')

class DepartmentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    code = StringField('Code', validators=[DataRequired()])
    level = SelectField('Level', choices=[('School', 'School'), ('College', 'College'), ('BS', 'BS')], validators=[DataRequired()])
    description = StringField('Description')
    submit = SubmitField('Add Department')

class FeeForm(FlaskForm):
    student_id = SelectField('Student', coerce=int, validators=[DataRequired()])
    amount_paid = StringField('Amount', validators=[DataRequired()])
    month = SelectField('Month', choices=[
        ('January', 'January'), ('February', 'February'), ('March', 'March'), 
        ('April', 'April'), ('May', 'May'), ('June', 'June'), 
        ('July', 'July'), ('August', 'August'), ('September', 'September'), 
        ('October', 'October'), ('November', 'November'), ('December', 'December')
    ], validators=[DataRequired()])
    year = StringField('Year', validators=[DataRequired()])
    payment_method = SelectField('Method', choices=[('Cash', 'Cash'), ('Bank', 'Bank'), ('Online', 'Online')], validators=[DataRequired()])
    submit = SubmitField('Collect Fee')

class ExamForm(FlaskForm):
    name = StringField('Exam Name', validators=[DataRequired()])
    session = StringField('Session', validators=[DataRequired()])
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Schedule Exam')

# Attendance is usually marked in bulk, so we might handle it differently or with a simple form first.
class AttendanceForm(FlaskForm):
    # This is a simplified single-student attendance form
    student_id = SelectField('Student', coerce=int, validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    status = SelectField('Status', choices=[('Present', 'Present'), ('Absent', 'Absent'), ('Leave', 'Leave')], validators=[DataRequired()])
    submit = SubmitField('Mark Attendance')
