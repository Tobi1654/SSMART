from app.extensions import db
from datetime import datetime
from flask_login import UserMixin
import bcrypt

# Creating the database for authenticating for all roles 

# User database model
class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), unique = True, nullable = False)
    password_hash = db.Column(db.String(60), nullable = False)
    role = db.Column(db.String(20), nullable = False) # change varchar to string in data validation table
    email = db.Column(db.String(100), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

# Started the authentication process for the user login, by making sure the password is secure

# set_password function takes the written password and hashes it with bcrypt, then stores the hash
    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

# check_password function, then takes the written password and compares it to the stored hashed password and checks if it matches
    def check_password(self, password):
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password_hash.encode('utf-8')
        )

#Student database model, links to users table and classes table
class Student(db.Model):
    __tablename__ = 'students'
    student_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable = False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.class_id'), nullable = False)
    full_name = db.Column(db.String(100), nullable = False)
    dob = db.Column(db.Date, nullable = False)
    date_enrolled = db.Column(db.DateTime, default = datetime.utcnow)

#teacher database models, links to users table
class Teacher(db.Model):
    __tablename__ = 'teachers'
    teacher_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable = False)
    full_name = db.Column(db.String(100), nullable = False)
    department = db.Column(db.String(50)) #note: change department under teachers to not be required
    subjects = db.Column(db.String(300))

#class database model, links to the teacher table
class Class(db.Model):
    __tablename__ = 'classes'
    class_id = db.Column(db.Integer, primary_key = True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.teacher_id'), nullable = False)
    class_name = db.Column(db.String(10), unique = True, nullable = False)
    year_group = db.Column(db.Integer, nullable = False)

#attendance database model, links to both student and class table
class Attendance(db.Model):
    __tablename__ = 'attendance'
    attendance_id = db.Column(db.Integer, primary_key = True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable = False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.class_id'), nullable = False)
    date = db.Column(db.Date, nullable = False) # ask mr parr, if datetime is best or just date
    status = db.Column(db.String(20), nullable = False)

#subject database model
class Subject(db.Model):
    __tablename__ = 'subjects'
    subject_id = db.Column(db.Integer, primary_key = True)
    subject_name = db.Column(db.String(100), unique = True, nullable = False)

#grades database model, links to both student and subject id
class Grade(db.Model):
    __tablename__  = 'grades'
    grade_id = db.Column(db.Integer, primary_key = True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable = False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.subject_id'), nullable = False)
    assessment_name = db.Column(db.String(100), nullable = False)
    max_score = db.Column(db.Integer, nullable = False)
    student_score = db.Column(db.Integer, nullable = False)
    percentage = db.Column(db.Float)
    letter_grade = db.Column(db.String(3)) # size 3 is supposed to be in the letter_grade
    date = db.Column(db.Date, nullable = False)
    feedback = db.Column(db.String(200)) # change the max size of feedback to 200

class Homework(db.Model):
    __tablename_ = 'homework'
    homework_id = db.Column(db.Integer, primary_key = True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.class_id'), nullable = False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.subject_id'), nullable = False)
    title = db.Column(db.String(100), nullable = False)
    description = db.Column(db.String(500))
    deadline = db.Column(db.Date, nullable = False)
    notification_sent = db.Column(db.Boolean, default = False)
    status = db.Column(db.String(20), nullable = False)

class SeatingPlan(db.Model):
    __tablename__ = 'seating_plan'
    seating_id = db.Column(db.Integer, primary_key = True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable = False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.class_id'), nullable = False)
    position_row = db.Column(db.Integer)
    position_col = db.Column(db.Integer)

class Notification(db.Model):
    __tablename__ = 'notifications'
    notification_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable = False)
    title = db.Column(db.String(100), nullable = False)
    message = db.Column(db.String(500), nullable = False)
    type = db.Column(db.String(20), nullable = False) # change datatype too string in data validation table
    read_status = db.Column(db.Boolean, default = False)
    created_at = db.Column(db.DateTime, default = datetime.utcnow)

class Message(db.Model):
    __tablename__ = 'messages'
    message_id = db.Column(db.Integer, primary_key = True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable = False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable = False)
    content = db.Column(db.String(30000), nullable = False)
    timestamp = db.Column(db.DateTime, default = datetime.utcnow)
    read_status = db.Column(db.Boolean, default = False)