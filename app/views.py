from flask import Blueprint, render_template

# blue print setting up
views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")
