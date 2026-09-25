from flask import Blueprint, url_for, request, flash, render_template, redirect
from app.extensions import db
from app.models import Teacher, Class, Student
from app.utils import teacher_required
from flask_login import current_user

teacher = Blueprint('teacher', __name__)

def get_current_teacher():
    return Teacher.query.filter_by(user_id=current_user.user_id).first()

@teacher.route('/teacher_dashboard')
@teacher_required
def dashboard():
    current_teacher = get_current_teacher()

    if not current_teacher:
        flash('You account is not logged to a teacher record', category='error')
        return redirect(url_for('auth.login'))

#this returns the classes that the teacher has been assigned
    assigned_class = Class.query.filter_by(teacher_id=current_teacher.teacher_id).all()

    return render_template(
        'teacher_dashboard.html',
        teacher = current_teacher,
        classes = assigned_class
    )