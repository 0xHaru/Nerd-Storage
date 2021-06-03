from flask import Blueprint, abort, request
from flask_login import login_required

from .handlers import delete_handler, download_handler, get_handler, post_handler

views = Blueprint("views", __name__)


@views.route("/", defaults={"path": ""}, methods=["GET"])
@views.route("/index", defaults={"path": ""}, methods=["GET", "POST"])
@views.route("/index/<path:path>", methods=["GET", "POST", "DELETE"])
@login_required
def index(path):
    if request.method == "GET":
        return get_handler(request, path)

    if request.method == "POST":
        return post_handler(request, path)

    if request.method == "DELETE":
        return delete_handler(request, path)

    return abort(405)


@views.route("/downloads", defaults={"path": ""}, methods=["GET"])
@views.route("/downloads/<path:path>", methods=["GET"])
@login_required
def download(path):
    if request.method == "GET":
        return download_handler(request, path)

    return abort(405)
