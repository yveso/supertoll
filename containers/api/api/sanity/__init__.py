from flask import Blueprint, jsonify

bp = Blueprint("sanity", __name__, url_prefix="/sanity")


@bp.route("/")
def index():
    resp = {"message": "Relax"}
    return jsonify(resp)
