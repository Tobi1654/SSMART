from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

#admin required section
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('You must be logged in', category='error')
            return redirect(url_for('auth.login'))

        if current_user.role != 'admin':
            flash('You do not have permission to access this page', category='error')
            return redirect(url_for('auth.login'))

        return f(*args, **kwargs)

    return decorated_function


# teacher required section
def teacher_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('You must be logged in', category='error')
            return redirect(url_for('auth.login'))

        if current_user.role != 'teacher':
            flash('You do not have permission to access this page', category='error')
            return redirect(url_for('auth.login'))

        return f(*args, **kwargs)

    return decorated_function

#student required section
# teacher required section
def student_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('You must be logged in', category='error')
            return redirect(url_for('auth.login'))

        if current_user.role != 'student':
            flash('You do not have permission to access this page', category='error')
            return redirect(url_for('auth.login'))

        return f(*args, **kwargs)

    return decorated_function