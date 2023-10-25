import json
import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from werkzeug.exceptions import HTTPException

from .models import db, migrate
from .config import Config


basedir = os.path.abspath(os.path.dirname(__file__))


bootstrap = Bootstrap()
login_manager = LoginManager()
bcrypt = Bcrypt()
csrf_protect = CSRFProtect()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    csrf_protect.init_app(app)

    # Blueprints
    from .auth import auth
    app.register_blueprint(auth)

    from .posts import posts
    app.register_blueprint(posts, url_prefix='/api')

    # Error handlers
    @app.errorhandler(HTTPException)
    def handle_exception(e):
        response = e.get_response()
        response.data = json.dumps({
            "code": e.code,
            "message": e.name,
            "description": e.description,
        })
        response.content_type = "application/json"
        return response

    return app
