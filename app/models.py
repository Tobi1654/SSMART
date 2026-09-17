from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy

# Creating the database for authenticating for all roles 
# User database model
class User(db.Model):
    __tablename__ = 'users'
    user_id = db.column(db.Integer, primary_key = True)
    username = db.column(db.String(100), unique = True, nullable = False)
    password_hash = db.column(db.String(60), nullable = False)
    role = db.column(db.String(20), nullable = False)
    email = db.column(db.String(100), nullable = False)
    date_created = db.column(db.DateTime, default = datetime.utcnow)

#Student database model, links to users table and classes table
class Student(db.Model):
    __tablename__ = 'students'
    student_id = db.column(db.Integer, primary_key = True)
    user_id = db.column(db.Integer, db.ForeignKey('users.user_id'), nullable = False)
    class_id = db.column(db.Integer, db.ForeignKey('classes.class_id'), nullable = False)
    full_name = db.column(db.String(100), nullable = False)
    dob = db.column(db.Date, nullable = False)
    date_enrolled = db.column(db.DateTime, default = datetime.utcnow)

#teacher database models, links to users table
class Teacher(db.Model):
    __tablename__ = 'teachers'
    teacher_id = db.column(db.Integer, primary_key = True)
    user_id = db.column(db.Integer, db.ForeignKey('users.user_id'), nullable = False)
    full_name = db.column(db.String(100), nullable = False)
    department = db.column(db.String(50)) #note: change department under teachers to not be required
    subjects = db.column(db.String(300))

#class database model, links to the teacher table
class Class(db.Model):
    __tablename__ = 'classes'
    class_id = db.column(db.Integer, primary_key = True)
    teacher_id = db.column(db.Integer, db.ForeignKey('teachers.teacher_id'), nullable = False)
    class_name = db.column(db.String(10), unique = True, nullable = False)
    year_group = db.column(db.Integer, nullable = False)

#attendance database model, links to both student and class table
class Attendance(db.Model):
    __tablename__ = 'attendance'
    attendance_id = db.column(db.Integer, primary_key = True)
    student_id = db.column(db.Integer, db.ForeignKey('students.student_id'), nullable = False)
    class_id = db.column(db.Integer, db.ForeignKey('classes.class_id'), nullable = False)
    date = db.column(db.Date, nullable = False) # ask mr parr, if datetime is best or just date
    status = db.column(db.String(20), nullable = False)

#subject database model
class Subject(db.Model):
    __tablename__ = 'subjects'
    subject_id = db.column(db.Integer, primary_key = True)
    subject_name = db.column(db.String(100), unique = True, nullable = False)

#grades database model, links to both student and subject id
class Grade(db.Model):
    __tablename__  = 'grades'
    grade_id = db.column(db.Integer, primary_key = True)
    student_id = db.column(db.Integer, db.ForeignKey('students.student_id'), nullable = False)
    subject_id = db.column(db.Integer, db.ForeignKey('subjects.subject_id'), nullable = False)
    assessment_name = db.column(db.String(100), nullable = False)
    max_score = db.column(db.Integer, nullable = False)
    student_score = db.column(db.Integer, nullable = False)
    percentage = db.column(db.Float)
    letter_grade = db.column(db.String(3)) # size 3 is supposed to be in the letter_grade
    date = db.column(db.Date, nullable = False)
    feedback = db.column(db.String(200)) # change the max size of feedback to 200

class Homework(db.Model):
    __tablename_ = 'homework'
    homework_id = db.column(db.Integer, primary_key = True)
    class_id = db.column(db.Integer, db.ForeignKey('classes.class_id'), nullable = False)
    subject_id = db.column(db.Integer, db.ForeignKey('subjects.subject_id'), nullable = False)
    title = db.column(db.String(100), nullable = False)
    description = db.column(db.String(500))
    deadline = db.column(db.Date, nullable = False)
    notification_sent = db.column(db.Boolean, default = False)
    status = db.column(db.String(20), nullable = False)

class SeatingPlan(db.Model):
    __tablename__ = 'seating_plan'
    seating_id = db.column(db.Integer, primary_key = True)
    student_id = db.column(db.Integer, db.ForeignKey('students.student_id'), nullable = False)
    class_id = db.column(db.Integer, db.ForeignKey('classes.class_id'), nullable = False)
    position_row = db.column(db.Integer)
    position_col = db.column(db.Integer)

class Notification(db.Model):
    __tablename__ = 'notifications'
    notification_id = db.column(db.Integer, primary_key = True)
    user_id = db.column(db.Integer, db.ForeignKey('users.user_id'), nullable = False)
    title = db.column(db.String(100), nullable = False)
    message = db.column(db.String(500), nullable = False)
    type = db.column(db.String(20), nullable = False) # change datatype too string in data validation table
    read_status = db.column(db.Boolean, default = False)
    created_at = db.column(db.DateTime, default = datetime.utcnow)

class Message(db.Model):
    __tablename__ = 'messages'
    message_id = db.column(db.Integer, primary_key = True)
    sender_id = db.column(db.Integer, db.ForeignKey('users.user_id'), nullable = False)
    recipient_id = db.column(db.Integer, db.ForeignKey('users.user_id'), nullable = False)
    content = db.column(db.String(30000), nullable = False)
    timestamp = db.column(db.DateTime, default = datetime.utcnow)
    read_status = db.column(db.Boolean, default = False)