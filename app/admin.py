from flask import Blueprint, url_for, request, flash, render_template, redirect
from app.extensions import db
from app.models import User, Teacher, Class, Student
from app.utils import admin_required
from datetime import datetime
import secrets
import string

admin = Blueprint('admin', __name__)

#function for generating a temporary password for the new user
def generate_temp_password(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

@admin.route('/admin_dashboard')
@admin_required
def dashboard():
    return render_template('admin_dashboard.html')

@admin.route('/admin/add_user', methods=['GET', 'POST'])
@admin_required
def add_user():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        role = request.form.get('role')
        class_id = request.form.get('class_id')
        dob = request.form.get('dob')
        department = request.form.get('department')
        subject = request.form.get('subject')

        if not full_name or not email or not role:
            flash('Full name, email, and role are required', category='error')
            return redirect(url_for('admin.add_user'))

        if '@' not in email:
            flash('Valid email is required', category='error')
            return redirect(url_for('admin.add_user'))

        if User.query.filter_by(email=email).first():
            flash('An account with this email already exist', category='error')
            return redirect(url_for('admin.add_user'))

        if role == 'student':
            if not dob or not class_id:
                flash('Date of birth and class are required for students', category='error')
                return redirect(url_for('admin.add_user'))

            if not Class.query.get(class_id):
                flash('Selected class does not exist', category='error')
                return redirect(url_for('admin.add_user'))

        base_username = email.split('@')[0]
        username = base_username
        counter = 1

        while User.query.filter_by(username=username).first():
            username = f'{base_username}{counter}'
            counter += 1

        temp_password = generate_temp_password()

        new_user = User(
            username=username,
            email=email,
            role= role
        )

        new_user.set_password(temp_password)
        db.session.add(new_user)
        db.session.flush()

        if role == 'teacher':
            new_teacher = Teacher(
                user_id = new_user.user_id,
                full_name = full_name,
                department = department,
                subjects = subject
            )
            db.session.add(new_teacher)

        elif role == 'student':
            from datetime import datetime
            dob_date = datetime.strptime(dob, '%Y-%m-%d').date()
            new_student = Student(
                user_id = new_user.user_id,
                full_name = full_name,
                dob = dob_date,
                class_id = int(class_id),
                date_enrolled = datetime.today().date()
            )
            db.session.add(new_student)

        db.session.commit()

        flash(f'{role} created. Username: {username} | Temp password: {temp_password}', category='success')
        return redirect(url_for('admin.add_user'))

    classes = Class.query.all()
    return render_template('add_user.html', classes=classes) 



@admin.route('/admin/add_class', methods=['POST', 'GET'])
@admin_required
def add_class():
    if request.method == 'POST':
        class_name = request.form.get('class_name')
        year_group = request.form.get('year_group')
        teacher_id = request.form.get('teacher_id')

        if not class_name or not year_group:
            flash('Class name and year group are required', category='error')
            return redirect(url_for('admin.add_class'))

        if Class.query.filter_by(class_name=class_name).first():
            flash('This class name already exists', category='error')
            return redirect(url_for('admin.add_class'))


        try:
            year_group_int = int(year_group)
            if year_group_int < 7 or year_group_int > 13:
                flash('Year group must be between 7and 13', category='error')
                return redirect(url_for('admin.add_class'))
        except ValueError:
            flash('Year group must be a number', category='error')
            return redirect(url_for('admin.add_class'))

        if teacher_id:
            teacher_id = int(teacher_id)
        else:
            teacher_id = None

        new_class = Class(
            class_name = class_name,
            year_group = year_group_int,
            teacher_id = teacher_id
        )
        db.session.add(new_class)
        db.session.commit()

        flash(f"Class: {class_name} created successfully", category='success')
        return redirect(url_for('admin.add_class'))

    teachers = Teacher.query.all()
    return render_template('add_class.html', teachers = teachers)

@admin.route('/admin/students')
@admin_required
def students():
    search_query = request.args.get('search', '').strip()
    class_filter = request.args.get('class_filter', '').strip()
    year_filter = request.args.get('year_filter', '').strip()

    query = Student.query

    if search_query:
        query = query.filter(Student.full_name.ilike(f'%{search_query}%'))

    if class_filter:
        query = query.filter(Student.class_id == int(class_filter))

    if year_filter:
        query = query.join(Class, Student.class_id == Class.class_id).filter(Class.year_group == int(year_filter))

    students_list = query.all()

    student_data = []
    for s in students_list:
        user = User.query.get(s.user_id)
        student_class = Class.query.get(s.class_id)
        student_data.append({
            'student_id': s.student_id,
            'full_name': s.full_name,
            'username': user.username if user else '-',
            'email': user.email if user else '-',
            'class_name': student_class.class_name if student_class else '-',
            'year_group': student_class.year_group if student_class else '-',
            'dob': s.dob,
            'date_enrolled': s.date_enrolled
        })

    classes = Class.query.all()

    return render_template(
        'students.html',
        students = student_data,
        classes = classes,
        search_query = search_query,
        class_filter = class_filter,
        year_filter  =year_filter
    )

@admin.route('/admin/edit_student/<int:student_id>', methods=['GET', 'POST'])
@admin_required
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)
    user = User.query.get(student.user_id)

    if request.method == "POST":
        full_name = request.form.get('full_name')
        dob = request.form.get('dob')
        email = request.form.get('email')
        class_id = request.form.get('class_id')

        if not full_name or not dob or not email or not class_id:
            flash('All fields are required', category='error')
            return redirect(url_for('admin.edit_student', student_id=student_id))

        if '@' not in email:
            flash('Valid email is required', category='error')
            return redirect(url_for('admin.edit_student', student_id=student_id))

        existing = User.query.filter_by(email=email).first()
        if existing and  existing.user_id != user.user_id:
            flash('This email already exists by another account', category='error')
            return redirect(url_for('admin.edit_student', student_id=student_id))

        if not Class.query.get(class_id):
            flash('The class you selected does not exists', category='error')
            return redirect(url_for('admin.edit_student', student_id=student_id))

        try:
            dob.date = datetime.strptime(dob, '%Y-%m-%d')
        except ValueError:
            flash('Invalid date of birth', category='error')
            return redirect(url_for('admin.edit_student', student_id=student_id))

        student.full_name = full_name
        student.dob = dob.date()
        student.class_id = int(class_id)
        user.email = email 

        db.session.commit()

        flash('Student account has been updated', category='success')
        return redirect(url_for('admin.students'))

    classes = Class.query.all()
    return render_template('edit_student.html', student=student, user=user, classes=classes)

@admin.route('/admin/delete_student/<int:student_id>', methods=['POST', 'GET'])