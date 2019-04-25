from flask import Blueprint
from flask_restful import Api, Resource

bp = Blueprint("users", __name__)
api = Api(bp)


class UsersPing(Resource):
    def get(self):
        return {"status": "success", "message": "hooray"}


api.add_resource(UsersPing, "/users/ping")
