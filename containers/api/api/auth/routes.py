from flask import jsonify, request
from sqlalchemy import exc, or_

from api import db, bcrypt
from api.auth import bp
from api.models import User


@bp.route("/register", methods=["POST"])
def register():
    post_data = request.get_json()

    if (
        not post_data
        or "username" not in post_data
        or "email" not in post_data
        or "password" not in post_data
    ):
        return jsonify({"message": "Invalid payload", "status": "fail"}), 400

    username = post_data.get("username")
    email = post_data.get("email")
    password = post_data.get("password")

    try:
        user = User.query.filter(
            or_(User.username == username, User.email == email)
        ).first()
        if not user:
            new_user = User(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            auth_token = new_user.encode_auth_token()
            return (
                jsonify(
                    {
                        "message": "Successfully registered",
                        "status": "success",
                        "auth_token": auth_token.decode(),
                    }
                ),
                201,
            )
        else:
            return (
                jsonify({"message": "User already exists", "status": "fail"}),
                400,
            )
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Database error", "status": "fail"}), 400


@bp.route("/login", methods=["POST"])
def login():
    post_data = request.get_json()

    if (
        not post_data
        or "email" not in post_data
        or "password" not in post_data
    ):
        return jsonify({"message": "Invalid payload", "status": "fail"}), 400

    email = post_data.get("email")
    password = post_data.get("password")

    try:
        user = User.query.filter_by(email=email).first()
        if user:
            if bcrypt.check_password_hash(user.password_hash, password):
                auth_token = user.encode_auth_token()
                return (
                    jsonify(
                        {
                            "status": "success",
                            "message": "Successfully logged in",
                            "auth_token": auth_token.decode(),
                        }
                    ),
                    200,
                )
            else:
                return (
                    jsonify({"status": "fail", "message": "Check password"}),
                    400,
                )
        else:
            return (
                jsonify({"status": "fail", "message": "User doesn't exist"}),
                404,
            )
    except Exception:
        return jsonify({"status": "fail", "message": "Try again"}), 500


@bp.route("/logout", methods=["GET"])
def logout():
    auth_header = request.headers.get("Authorization")
    if auth_header:
        auth_token = auth_header.split(" ")[1]
        response = User.decode_auth_token(auth_token)
        if not isinstance(response, str):
            return (
                jsonify(
                    {"status": "success", "message": "Successfully logged out"}
                ),
                200,
            )
        else:
            return jsonify({"status": "fail", "message": response}), 401
    else:
        return jsonify({"status": "fail", "message": "Missing header"}), 403


@bp.route("/status", methods=["GET"])
def status():
    auth_header = request.headers.get("Authorization")
    if auth_header:
        auth_token = auth_header.split(" ")[1]
        response = User.decode_auth_token(auth_token)
        if not isinstance(response, str):
            user = User.query.filter_by(id=response).first()
            return (
                jsonify(
                    {
                        "status": "success",
                        "message": "Success",
                        "data": user.to_json(),
                    }
                ),
                200,
            )
        else:
            return jsonify({"status": "fail", "message": response}), 401
    else:
        return jsonify({"status": "fail", "message": "Invalid token"}), 401
