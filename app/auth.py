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

#routing to the sign up page
@auth.route('/logout')
def logout():
    return "Logging out..."
