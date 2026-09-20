from flask import Blueprint, render_template, request, flash, url_for, redirect
from app.models import User
from flask_login import login_user, logout_user, login_required
from app.extensions import db

# blue print setting up for auth
auth = Blueprint('auth', __name__)

## routing to the login page
@auth.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        selected_role = request.form.get('role')

    #if len(username) < 4:
    #   flash('Username is too short', category='error')
    
    #else:
    #   flash('Successfully logged in', category = 'success')

        if not username or not password or not selected_role:
                flash('All fields are required', category='error')
                return redirect(url_for('auth.login'))
        

        user = User.query.filter_by(username = username).first()

        if not user:
            flash('User not found', category='error')
            return redirect(url_for('auth.login'))

        if not user.check_password(password):
            flash('Incorrect Password', category='error')
            return redirect(url_for('auth.login'))

        if user.role != selected_role:
            flash('Account cannot log in with selected role', category='error')
            return redirect(url_for('auth.login'))

        login_user(user)

        if user.role == 'student':
            return redirect(url_for('auth.student_dashboard'))
        elif user.role == 'teacher':
            return redirect(url_for('auth.teacher_dashboard'))
        elif user.role == 'admin':
            return redirect(url_for('admin.dashboard'))

    return render_template("login.html")

@auth.route('/student_dashboard')
@login_required
def student_dashboard():
    return 'Student Dashboard'

@auth.route('/teacher_dashboard')
@login_required
def teacher_dashboard():
    return 'Teacher Dashboard'

#@auth.route('/admin_dashboard')
#@login_required
#def admin_dashboard():
    #return 'Admin Dashboard'

#routing to the log in page
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', category='success')
    return redirect(url_for('auth.login'))
