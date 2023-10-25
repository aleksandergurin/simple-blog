from http import HTTPStatus

from pydantic import ValidationError
from flask import (
    jsonify,
    request,
    Blueprint,
)
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_wtf.csrf import generate_csrf

from .validators import UserValidator, LoginValidator
from .models import User, db
from . import login_manager, bcrypt

auth = Blueprint("auth", __name__)


@login_manager.user_loader
def user_loader(user_id):
    user = User.query.get(user_id)
    return user


@auth.route("/auth/register", methods=["POST"])
def user_register():
    try:
        user_input = UserValidator.parse_raw(request.data)
    except ValidationError as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST

    user_exists = User.query.filter(User.username == user_input.username).first()
    if user_exists:
        return jsonify({"message": "Specified name already taken"}), 409

    password_hash = bcrypt.generate_password_hash(user_input.password).decode()
    user = User(
        email=user_input.email,
        username=user_input.username,
        password_hash=password_hash,
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({
        "user_id": user.user_id,
        "message": "User created",
    }), HTTPStatus.CREATED


@auth.route("/auth/login", methods=["POST"])
def login():
    try:
        login_input = LoginValidator.parse_raw(request.data)
    except ValidationError as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST

    user = User.query.filter(User.username == login_input.username).first()

    error_resp = {
        "isAuthenticated": False,
        "message": "Incorrect username or password",
    }

    if not user:
        return jsonify(error_resp), HTTPStatus.BAD_REQUEST

    if user and bcrypt.check_password_hash(user.password_hash, login_input.password):
        login_user(user)

        return jsonify({
            "isAuthenticated": True,
            "message": "Logged in",
        })

    return jsonify(error_resp)


@auth.route("/auth/logout")
@login_required
def logout():
    logout_user()
    return jsonify({
        "isAuthenticated": False,
        "message": "Logged out",
    })


@auth.route("/auth/is-authenticated")
def check_session():
    if current_user.is_authenticated:
        return jsonify({"isAuthenticated": True})

    return jsonify({"isAuthenticated": False})


@auth.route("/auth/csrf", methods=["GET"])
def get_csrf():
    token = generate_csrf()
    response = jsonify({"message": "CSRF cookie set"})
    response.headers.set("X-CSRFToken", token)
    return response
