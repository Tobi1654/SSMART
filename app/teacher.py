from flask import Blueprint, url_for, request, flash, render_template, redirect
from app.extensions import db
from app.models import Teacher, Class, Student, Attendance, Subject, Grade
from app.utils import teacher_required
from flask_login import current_user
from datetime import date
from app.attendance_calculating import calculate_attendance_percentage, create_attendance_flag

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

@teacher.route('/teacher/attendance/<int:class_id>')
@teacher_required
def attendance(class_id):
    current_teacher =get_current_teacher()
    classroom = Class.query.get_or_404(class_id)

    if classroom.teacher_id != current_teacher.teacher_id:
        flash('Can only mark attendance for your class', category='error')
        return redirect(url_for('teacher.dashboard'))

    students = Student.query.filter_by(class_id=class_id).all()

    today = date.today()
    existing = Attendance.query.filter_by(class_id=class_id, date=today).all()

    existing_statuses = {a.student_id: a.status for a in existing}
    existing_actions = {a.student_id: a.actions for a in existing if a.actions}

    return render_template(
        'attendance.html',
        classroom=classroom,
        students=students,
        existing_statuses=existing_statuses,
        existing_actions=existing_actions,
        today=today
    )

@teacher.route('/teacher/attendance/<int:class_id>/save', methods = ['POST'])
@teacher_required
def save_attendance(class_id):
    current_teacher = get_current_teacher()
    classroom = Class.query.get_or_404(class_id)

    if classroom.teacher_id != current_teacher.teacher_id:
        flash('You can only mark the attendance of your own class', category='error')
        return redirect(url_for('teacher.dashboard'))

    students  = Student.query.filter_by(class_id=class_id).all()
    today = date.today()

    Attendance.query.filter_by(class_id=class_id, date=today).delete()

    for student in students:
        status = request.form.get(f'status_{student.student_id}')
        actions = request.form.get(f'actions_{student.student_id}','').strip()

        if status in ['present', 'late', 'absent']:
            record = Attendance(
                student_id = student.student_id,
                class_id=class_id,
                date=today,
                status=status,
                actions=actions if actions else None
            )
            db.session.add(record)

    db.session.commit()

    for student in  students: # every time the attendance is saved, each student get their percentage recalculated, which is then stored in the student record
        percentage = calculate_attendance_percentage(student.student_id)
        student.attendance_percentage = percentage
    db.session.commit()

    #creates the flag notification for the students under the 80% threshold
    for student in students:
        create_attendance_flag(student.student_id, class_id)

    flash('Attendance saved successfully', category='success')
    return redirect(url_for('teacher.dashboard'))

@teacher.route('/teacher/grades/<int:class_id>/<subject>/enter', methods=['GET','POST'])
@teacher_required
def enter_grades(subject, class_id):
    current_teacher = get_current_teacher()
    classroom = Class.query.get_or_404(class_id)

    if classroom.teacher_id != current_teacher.teacher_id: #this checks if the teacher entering the garde does teach this class
        flash('You are only able to enter grades for your own class', category='error')
        return redirect(url_for('teacher.dashboard'))

    students = Student.query.filter_by(class_id=class_id).all()

    if request.method == 'POST':
        assessment_name = request.form.get('assessment_name', '').strip()
        max_score = request.form.get('max_score','').strip()
        assessment_date = request.form.get('assessment_date')


        if not assessment_date or not assessment_name or not max_score: #this validates that all field are required
            flash('All fields are required', category='error')
            return redirect(url_for('teacher.enter_grades', class_id=class_id, subject=subject))

            try:
                max_score_int = int(max_score)
                if max_score <= 0:
                    raise ValueError
            except ValueError:
                flash('Invalid max_score, must be greater than 0', 'error')
                return redirect(url_for('teacher.enter_grades', class_is=class_id, subject=subject))

            

