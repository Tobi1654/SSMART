from flask import Blueprint, render_template, request

# blue print setting up for auth
auth = Blueprint('auth', __name__)

## routing to the login page
@auth.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        selected_role = request.form.get('role')
    return render_template("login.html")

    user = User.query.filter_by(username=username).first()

    if not user:
        flash('User not found', 'error')
        return redirect(url_for('auth.login'))

    if not user.check_password(password):
        flash('Incorrect Password', 'error')
        return redirect(url_for('auth.login'))

    if user.role != selected_role:
        flash('Account cannot log in with selected role', 'error')
        return redirect(url_for('auth.login'))

#routing to the sign up page
@auth.route('/logout')
def logout():
    return "Logging out..."
