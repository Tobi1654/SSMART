from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy

# Creating the database for authenticating for all roles, so basically the user model
class User(db.Model):
    __tablename__ = 'users'
    user_id = db.column(db.Integer, primary_key = True)
    username = db.column(db.String(100), unique = True, nullable = False)
    password_hash = db.column(db.String(60), nullable = False)
    role = db.column(db.varchar(20), nullable = False)
    email = db.column(db.String(100), nullable = False)
    date_created = db.column(db.DateTime, default = datetime.utcnow)

class Student(db.Model):

class Teacher(db.Model):

class Class(db.Model):

class Attendance(db.Model):

class Subject(db.Model):

class Grade(db.Model):

class Homework(db.Model):

class SeatingPlan(db.Model):

class Notification(db.Model):

class Message(db.Model):

