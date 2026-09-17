from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-key-change-this-later'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ssmart.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.int_app(app)

    from app import models

    with app.app_context():
        db.create_all()


    @app.route('/')
    def home():
        return "SSMART is running"

    return app