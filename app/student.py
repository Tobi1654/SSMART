from flask import Blueprint, url_for, request, flash, render_template, redirect
from app.extensions import db
from app.models import Student, Class, Student, Attendance, Subject, Grade, Homework
from app.utils import student_required
from flask_login import current_user
from datetime import date

student = Blueprint('student', __name__)

def get_current_student(): #fetches the student that is currently logged in
    return Student.query.filter_by(user_id=current_user.user_id).first()

#routes the logged in student to their dashboard
@student.route('/student_dashboard')
@student_required
def dashboard():
    current_student = get_current_student()

    if not current_student:
        flash('You account is not logged to a student record', category='error')
        return redirect(url_for('auth.login'))

    attendance_percentage = current_student.attendance_percentage or 0

    

