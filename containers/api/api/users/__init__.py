from flask import Blueprint

bp = Blueprint("users", __name__)

from api.users import resources  # noqa
