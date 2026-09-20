from flask import Blueprint, url_for, request, flash, render_template, redirect
from app.extensions import db
from app.models import User, Teacher
from app.utils import admin_required
import secrets
import string

admin = Blueprint('admin', __name__)

def generate_temp_password(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

@admin.route('/admin/dashboard')
@admin_required
def dashboard():
    return render_template('admin_dashboard.html')

admin.route('/admin/add_teacher', method=['GET', 'POST'])
@admin_required
def add_teacher():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        department = request.form.get('department')
        subject = request.form.get('subject')

        if not full_name or not email:
            flash('Full name and email are required', category='error')
            return redirect(url_for('admin.add_teacher'))

        if User.query.filter_by(email=email).first():
            flash('An account with this email already exist', category='error')
            return redirect(url_for('admin.add_teacher'))

        base_username = email.split('@')[0]
        username = base_username
        counter = 1

        while User.query.filter_by(username=username).first():
            username = f'{base_username}{counter}'
            counter += 1

        temp_password = generate_temp_password

        new_user = User(
            username=username,
            email=email,
            role='teacher'
        )

        new_user.set_password(temp_password)
        db.session.add(new_user)
        db.session.flush

        new_teacher = Teacher(
            user_id = new_user.user_id,
            full_name = full_name,
            department = department,
            subjects = subject
        )

        db.session.add(new_teacher)
        db.session.commit

        flash(f'Teacher created. Username: {username} | Temp password: {temp_password}', category='success')
        return redirect(url_for('admin.add_teacher'))

    return render_template('add_teacher.html')