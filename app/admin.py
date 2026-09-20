from flask import Blueprint, url_for, request, flash, render_template, redirect
from app.extensions import db
from app.models import User, Teacher, Class
from app.utils import admin_required
import secrets
import string

admin = Blueprint('admin', __name__)

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

        db.session.commit()

        flash(f'{role} created. Username: {username} | Temp password: {temp_password}', category='success')
        return redirect(url_for('admin.add_user'))

    return render_template('add_user.html') 

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
            teacher_id_int = int(teacher_id)
        else:
            teacher_id = None

        new_class = Class(
            class_name = class_name,
            year_group = year_group,
            teacher_id = teacher_id
        )
        db.session.add(new_class)
        db.session.commit()

        flash(f"Class: {class_name} created successfully", category='success')
        return redirect(url_for(admin.add_class))

    teachers = Teacher.query.all()
    return render_template('add_class.html', teachers = teachers)