from flask import Blueprint, url_for, request, flash, render_template, redirect
from app.extensions import db
from app.models import Student, Class, Student, Attendance, Subject, Grade, Homework, Notification
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

    #gets the attendance from the student record
    attendance_percentage = current_student.attendance_percentage or 0

    #gets all recorded grades and arranges them from the newest to oldest
    raw_grades = Grade.query.filter_by(student_id=student.student_id).order_by(Grade.date.desc()).all()

    grades = []
    for g in raw_grades:
        subject  = Subject.query.get(g.subject_id)

        grades.append({
            'subject_name': subject.subject_name if subject else '-',
            'assessment_name': g.assessment_name,
            'percentage': g.percentage,
            'letter_grade': g.letter_grade,
            'date': g.date,
        })

#this gets the average percentage for each subject
    subject_totals = {}
    subject_counts = {}

    for g in raw_grades:
        subject  = Subject.query.get(g.subject_id)
        name = subject.subject_name if subject else '-'

        if name not in subject_totals:
            subject_totals[name] = 0
            subject_counts[name] = 0

        subject_totals[name] = subject_totals[name] + g.percentage
        subject_counts[name] = subject_counts[name] + 1

        subject_averages = {}
        for name in subject_totals:
            average = subject_totals[name] / subject_counts[name]
            subject_averages[name] =round(average,2)

    #gets the homeworks and orders them by their deadline
    homeworks = Homework.query.filter_by(class_id=current_student.class_id).order_by(Homework.deadline).all()
    
    homework_data = []
    for hw in homeworks:
        subject  = Subject.query.get(hw.subject_id)
        days_left = ((hw.deadline) - (date.today())).days
        
        homework_data.append({
            'title': hw.title,
            'description': hw.description,
            'subject_name': subject.subject_name if subject else '-',
            'deadline': hw.deadline,
            'days_left': days_left
        })

    #gets the notifications and limits them to 3 so it is not every where
    notifications = Notification.query.filter_by(user=current_user.user_id).order_by(Notification.created_at.desc()).limit(3).all()

    return render_template(
        'student_dashboard.html',
        student = current_student,
        attendance_percentage = attendance_percentage,
        grades = grades,
        subject_averages = subject_averages,
        homeworks = homework_data,
        notifications = notifications,
        today = date.today()
    )