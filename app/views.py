from flask import Blueprint

# blue print setting up
views = Blueprint('views', __name__)

@views.route('/')
def home():
    return "Test"
