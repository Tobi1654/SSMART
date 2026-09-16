from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-key-change-this-later'

    @app.route('/')
    def home():
        return "SSMART is running"

    return app