from flask import Blueprint

# blue print setting up for auth
auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return "Login Page"

@auth.route('/logout')
def logout():
    return "Logging out..."
