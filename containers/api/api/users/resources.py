from flask import request
from flask_restful import Api, Resource

from api import db
from api.models import User
from api.users import bp

api = Api(bp)


class UsersPing(Resource):
    def get(self):
        return {"status": "success", "message": "hooray"}


class Users(Resource):
    def post(self):
        post_data = request.get_json()
        username = post_data.get("username")
        email = post_data.get("email")
        db.session.add(User(username=username, email=email))
        db.session.commit()

        return {"status": "success", "message": f"{email} was added!"}, 201


api.add_resource(UsersPing, "/users/ping")
api.add_resource(Users, "/users")
