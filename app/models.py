from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.extensions import db, login_manager

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='user') # admin, teacher, accountant, student, parent
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    level = db.Column(db.String(50)) # School, College, BS
    hod_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    teachers = db.relationship('Teacher', foreign_keys='Teacher.department_id', backref='department', lazy='dynamic')
    students = db.relationship('StudentAcademic', backref='department', lazy='dynamic')

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    reg_no = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    father_name = db.Column(db.String(100))
    cnic = db.Column(db.String(20), unique=True)
    dob = db.Column(db.Date)
    gender = db.Column(db.String(10))
    contact = db.Column(db.String(20))
    email = db.Column(db.String(120))
    address = db.Column(db.Text)
    photo_path = db.Column(db.String(200))
    admission_date = db.Column(db.Date, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Active') # Active, Passout, Dropout
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    academic_record = db.relationship('StudentAcademic', backref='student', uselist=False, cascade="all, delete-orphan")
    fee_payments = db.relationship('FeePayment', backref='student', lazy='dynamic')
    attendance = db.relationship('Attendance', backref='student', lazy='dynamic')
    marks = db.relationship('Mark', backref='student', lazy='dynamic')
    issued_books = db.relationship('BookIssue', backref='student', lazy='dynamic')
    transport = db.relationship('StudentTransport', backref='student', uselist=False)

class StudentAcademic(db.Model):
    __tablename__ = 'student_academic'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    class_level = db.Column(db.String(50)) # Class 10, FSc Part 1, BS Semester 1
    section = db.Column(db.String(10))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    roll_no = db.Column(db.String(20))
    session = db.Column(db.String(20))
    cgpa = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    father_name = db.Column(db.String(100))
    cnic = db.Column(db.String(20), unique=True)
    dob = db.Column(db.Date)
    gender = db.Column(db.String(10))
    contact = db.Column(db.String(20))
    email = db.Column(db.String(120))
    address = db.Column(db.Text)
    photo_path = db.Column(db.String(200))
    qualification = db.Column(db.String(100))
    designation = db.Column(db.String(50))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    joining_date = db.Column(db.Date)
    basic_salary = db.Column(db.Float)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    attendance = db.relationship('TeacherAttendance', backref='teacher', lazy='dynamic')
    salary_records = db.relationship('SalaryRecord', backref='teacher', lazy='dynamic')

class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    credit_hours = db.Column(db.Integer)
    description = db.Column(db.Text)

class ClassSection(db.Model):
    __tablename__ = 'class_sections'
    id = db.Column(db.Integer, primary_key=True)
    class_level = db.Column(db.String(50))
    section = db.Column(db.String(10))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    class_teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    academic_year = db.Column(db.String(20))
    
    timetable = db.relationship('Timetable', backref='class_section', lazy='dynamic')

class FeeStructure(db.Model):
    __tablename__ = 'fee_structure'
    id = db.Column(db.Integer, primary_key=True)
    class_level = db.Column(db.String(50))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    tuition_fee = db.Column(db.Float, default=0.0)
    admission_fee = db.Column(db.Float, default=0.0)
    exam_fee = db.Column(db.Float, default=0.0)
    lab_fee = db.Column(db.Float, default=0.0)
    library_fee = db.Column(db.Float, default=0.0)
    transport_fee = db.Column(db.Float, default=0.0)
    sports_fee = db.Column(db.Float, default=0.0)
    total_fee = db.Column(db.Float, default=0.0)
    academic_year = db.Column(db.String(20))

class FeePayment(db.Model):
    __tablename__ = 'fee_payments'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    receipt_no = db.Column(db.String(50), unique=True)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    month = db.Column(db.String(20))
    year = db.Column(db.String(10))
    amount_paid = db.Column(db.Float)
    payment_method = db.Column(db.String(50)) # Cash, Bank, Online
    late_fee = db.Column(db.Float, default=0.0)
    discount = db.Column(db.Float, default=0.0)
    remarks = db.Column(db.Text)
    received_by = db.Column(db.String(50)) # Username or Teacher Name
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Attendance(db.Model):
    __tablename__ = 'attendance'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class_sections.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id')) # For subject-wise tracking
    status = db.Column(db.String(20)) # Present, Absent, Leave, Late
    marked_by = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TeacherAttendance(db.Model):
    __tablename__ = 'teacher_attendance'
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20))
    remarks = db.Column(db.String(200))
    marked_by = db.Column(db.String(50))

class LeaveApplication(db.Model):
    __tablename__ = 'leave_applications'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer) # Can be student_id or teacher_id
    user_type = db.Column(db.String(20)) # 'student' or 'teacher'
    leave_type = db.Column(db.String(50))
    from_date = db.Column(db.Date)
    to_date = db.Column(db.Date)
    reason = db.Column(db.Text)
    status = db.Column(db.String(20), default='Pending') # Pending, Approved, Rejected
    approved_by = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Exam(db.Model):
    __tablename__ = 'exams'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100)) # Mid Term, Final
    exam_type = db.Column(db.String(50))
    class_level = db.Column(db.String(50))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    academic_year = db.Column(db.String(20))
    
    exam_subjects = db.relationship('ExamSubject', backref='exam', lazy='dynamic')

class ExamSubject(db.Model):
    __tablename__ = 'exam_subjects'
    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    exam_date = db.Column(db.Date)
    total_marks = db.Column(db.Float)
    passing_marks = db.Column(db.Float)

class Mark(db.Model):
    __tablename__ = 'marks'
    id = db.Column(db.Integer, primary_key=True)
    exam_subject_id = db.Column(db.Integer, db.ForeignKey('exam_subjects.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    obtained_marks = db.Column(db.Float)
    grade = db.Column(db.String(5))
    remarks = db.Column(db.String(200))

class SalaryRecord(db.Model):
    __tablename__ = 'salary_records'
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    month = db.Column(db.String(20))
    year = db.Column(db.String(10))
    basic_salary = db.Column(db.Float)
    allowances = db.Column(db.Float)
    deductions = db.Column(db.Float)
    net_salary = db.Column(db.Float)
    payment_date = db.Column(db.Date)
    payment_status = db.Column(db.String(20)) # Paid, Pending

class Timetable(db.Model):
    __tablename__ = 'timetable'
    id = db.Column(db.Integer, primary_key=True)
    class_section_id = db.Column(db.Integer, db.ForeignKey('class_sections.id'))
    day = db.Column(db.String(20))
    period = db.Column(db.Integer)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    room = db.Column(db.String(50))

class LibraryBook(db.Model):
    __tablename__ = 'library_books'
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(20))
    title = db.Column(db.String(200))
    author = db.Column(db.String(100))
    publisher = db.Column(db.String(100))
    category = db.Column(db.String(50))
    quantity = db.Column(db.Integer)
    available = db.Column(db.Integer)
    location = db.Column(db.String(50))

class BookIssue(db.Model):
    __tablename__ = 'book_issues'
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('library_books.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    issue_date = db.Column(db.Date)
    due_date = db.Column(db.Date)
    return_date = db.Column(db.Date)
    fine_amount = db.Column(db.Float)
    status = db.Column(db.String(20)) # Issued, Returned

class TransportRoute(db.Model):
    __tablename__ = 'transport_routes'
    id = db.Column(db.Integer, primary_key=True)
    route_name = db.Column(db.String(100))
    route_number = db.Column(db.String(20))
    driver_name = db.Column(db.String(100))
    driver_contact = db.Column(db.String(20))
    vehicle_number = db.Column(db.String(20))
    capacity = db.Column(db.Integer)

class StudentTransport(db.Model):
    __tablename__ = 'student_transport'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    route_id = db.Column(db.Integer, db.ForeignKey('transport_routes.id'))
    pickup_point = db.Column(db.String(100))
    monthly_fee = db.Column(db.Float)

class Announcement(db.Model):
    __tablename__ = 'announcements'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    target_audience = db.Column(db.String(50)) # All, Students, Teachers, Parents
    attachment = db.Column(db.String(200))
    posted_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    posted_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

class AcademicCalendar(db.Model):
    __tablename__ = 'academic_calendar'
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(200))
    event_type = db.Column(db.String(50)) # Holiday, Exam, Event
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    description = db.Column(db.Text)

class Achievement(db.Model):
    __tablename__ = 'achievements'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    achievement_type = db.Column(db.String(50))
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    date = db.Column(db.Date)
    certificate_path = db.Column(db.String(200))

class DisciplinaryRecord(db.Model):
    __tablename__ = 'disciplinary_records'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    incident_date = db.Column(db.Date)
    incident_type = db.Column(db.String(100))
    description = db.Column(db.Text)
    action_taken = db.Column(db.Text)
    recorded_by = db.Column(db.String(50))
