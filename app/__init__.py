from flask import Flask
from app.extensions import db, login_manager

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'I LoVe doNuTs'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ssmart.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app) # hooks flask login into my app
    login_manager.login_view = 'auth.login' # when user visits page when logged, it redirects them to  auth.login

    from app import models
    from app.models import User

# tells flask how to find a user form their ID
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id)) # then fetches that user form  the database using their primary key

    with app.app_context():
        db.create_all()

# defining the route in init.py
    from .views import views
    from .auth import auth

# defined the url prefixes
    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')


    @app.route('/')
    def home():
        return "SSMART is running"

    return app