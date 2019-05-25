from flask import request
from flask_restful import Api, Resource
from sqlalchemy import exc

from api import db
from api.models import User
from api.users import bp

api = Api(bp)


class UsersPing(Resource):
    def get(self):
        return {"status": "success", "message": "hooray"}


class Users(Resource):
    def get(self):
        return (
            {
                "status": "success",
                "data": {
                    "users": [user.to_json() for user in User.query.all()]
                },
            },
            200,
        )

    def post(self):
        post_data = request.get_json()

        if (
            not post_data
            or "username" not in post_data
            or "email" not in post_data
            or "password" not in post_data
        ):
            return {"message": "Invalid payload", "status": "fail"}, 400

        username = post_data.get("username")
        email = post_data.get("email")
        password = post_data.get("password")

        try:
            user_with_mail = User.query.filter_by(email=email).first()
            if not user_with_mail:
                db.session.add(
                    User(username=username, email=email, password=password)
                )
                db.session.commit()
                return (
                    {"status": "success", "message": f"{email} was added!"},
                    201,
                )
            else:
                return (
                    {"status": "fail", "message": "Email already exists."},
                    400,
                )
        except exc.IntegrityError:
            db.session.rollback()
            return {"message": "Database error", "status": "fail"}, 400


class UsersId(Resource):
    def get(self, user_id):
        error = {"status": "fail", "message": "User does not exist."}
        if not str(user_id).isdigit():
            return error, 404
        try:
            user = User.query.filter_by(id=user_id).first()
            if not user:
                return error, 404
            else:
                return ({"status": "success", "data": user.to_json()}, 200)
        except ValueError:
            return error, 404


api.add_resource(UsersPing, "/users/ping")
api.add_resource(Users, "/users")
api.add_resource(UsersId, "/users/<user_id>")
