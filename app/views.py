from flask import Blueprint

# blue print setting up
views = Blueprint('views', __name__)

@views.route('/')
def home():
    return "<h1>Test</h1>"
