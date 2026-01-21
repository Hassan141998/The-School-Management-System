from app import create_app, db
from app.models import User, Student, Teacher, Department, FeePayment, StudentAcademic
from faker import Faker
import random
from datetime import datetime

app = create_app()
fake = Faker()

def seed_data():
    with app.app_context():
        print("Creating tables...")
        db.create_all()
        
        # 1. Create Departments
        print("Seeding Departments...")
        depts = [
            ('Science', 'SCI', 'School', 'General Science Group'),
            ('Arts', 'ART', 'School', 'Humanities Group'),
            ('Computer Science', 'CS', 'BS', 'BS Computer Science'),
            ('English', 'ENG', 'BS', 'BS English Literature'),
            ('Physics', 'PHY', 'BS', 'BS Physics'),
            ('Pre-Medical', 'PM', 'College', 'FSc Pre-Medical'),
            ('Pre-Engineering', 'PE', 'College', 'FSc Pre-Engineering'),
            ('Commerce', 'COM', 'College', 'I.Com'),
            ('Mathematics', 'MATH', 'BS', 'BS Mathematics'),
            ('Business Admin', 'BBA', 'BS', 'BBA Program'),
            ('Biology', 'BIO', 'BS', 'BS Biology'),
            ('Chemistry', 'CHEM', 'BS', 'BS Chemistry'),
            ('Primary', 'PRI', 'School', 'Primary Section'),
            ('Middle', 'MID', 'School', 'Middle Section'),
            ('Playgroup', 'PG', 'School', 'Early Education')
        ]
        
        dept_objects = []
        for name, code, level, desc in depts:
            dept = Department.query.filter_by(code=code).first()
            if not dept:
                dept = Department(name=name, code=code, level=level, description=desc)
                db.session.add(dept)
                dept_objects.append(dept)
            else:
                dept_objects.append(dept)
        db.session.commit()

        # 2. Create Teachers
        print("Seeding Teachers...")
        teachers = []
        for i in range(25):
            emp_id = f'EMP{100+i}'
            if not Teacher.query.filter_by(employee_id=emp_id).first():
                dept = random.choice(dept_objects)
                teacher = Teacher(
                    employee_id=emp_id,
                    name=fake.name(),
                    email=fake.email(),
                    contact=fake.phone_number(),
                    qualification=random.choice(['PhD', 'MPhil', 'Masters', 'Bachelors']),
                    designation=random.choice(['Professor', 'Lecturer', 'Assistant Professor', 'Teacher']),
                    department_id=dept.id,
                    joining_date=fake.date_between(start_date='-5y', end_date='today'),
                    basic_salary=random.randint(40000, 150000)
                )
                db.session.add(teacher)
                teachers.append(teacher)
        db.session.commit()

        # 3. Create Students
        print("Seeding Students...")
        for i in range(120):
            reg = f'REG-2024-{1000+i}'
            if not Student.query.filter_by(reg_no=reg).first():
                student = Student(
                    reg_no=reg,
                    name=fake.name(),
                    father_name=fake.name_male(),
                    cnic=fake.ssn(),
                    dob=fake.date_of_birth(minimum_age=4, maximum_age=25),
                    contact=fake.phone_number(),
                    email=fake.email(),
                    address=fake.address(),
                    admission_date=fake.date_between(start_date='-2y', end_date='today'),
                    status='Active'
                )
                db.session.add(student)
                db.session.flush() # to get ID
                
                # Assign to Academic Record
                dept = random.choice(dept_objects)
                acad = StudentAcademic(
                    student_id=student.id,
                    class_level=dept.level,
                    section=random.choice(['A', 'B', 'C']),
                    department_id=dept.id,
                    roll_no=f'R-{student.id}',
                    session='2024-2025',
                    cgpa=round(random.uniform(2.0, 4.0), 2)
                )
                db.session.add(acad)
                
                # Fee Payments
                for m in range(1, 4):
                    payment = FeePayment(
                        student_id=student.id,
                        receipt_no=f'REC-{student.id}-{m}-{random.randint(1000,9999)}',
                        amount_paid=random.choice([5000, 10000, 15000]),
                        month=datetime(2025, m, 1).strftime('%B'),
                        year='2025',
                        payment_method='Cash',
                        received_by='admin'
                    )
                    db.session.add(payment)
        
        db.session.commit()
        print("Data seeding completed!")

if __name__ == '__main__':
    seed_data()
