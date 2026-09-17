from flask import Blueprint

# blue print setting up for auth
auth = Blueprint('auth', __name__)

## routing to the  login page
@auth.route('/login')
def login():
    return "Login Page"

#routing to the sign up page
@auth.route('/logout')
def logout():
    return "Logging out..."
