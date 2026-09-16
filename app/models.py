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
    role = db.column(db.varchar(20), nullable = False)
    email = db.column(db.String(100), nullable = False)
    date_created = db.column(db.DateTime, default = datetime.utcnow)

#Student database model, links to users table and classes table
class Student(db.Model):
    __tablename__ = 'students'
    student_id = db.column(db.Integer, primary_key = True)
    user_id = db.column(db.Integer, db.foreign_key('users.user_id'), nullable = False)
    class_id = db.column(db.Integer, db.foreign_key('classes.class_id'), nullable = False)
    full_name = db.column(db.String(100), nullable = False)
    dob = db.column(db.Date, nullable = False)
    date_enrolled = db.column(db.DateTime, default = datetime.utcnow)

class Teacher(db.Model):

class Class(db.Model):

class Attendance(db.Model):

class Subject(db.Model):

class Grade(db.Model):

class Homework(db.Model):

class SeatingPlan(db.Model):

class Notification(db.Model):

class Message(db.Model):