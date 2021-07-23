from flask import Blueprint, abort, render_template, request
from flask_login import current_user, login_required

from .handlers import (
    download_get_handler,
    index_delete_handler,
    index_get_handler,
    index_post_handler,
    large_file_get_handler,
    large_file_post_handler,
)

views = Blueprint("views", __name__)


@views.route("/", defaults={"path": ""}, methods=["GET"])
@views.route("/index", defaults={"path": ""}, methods=["GET", "POST"])
@views.route("/index/<path:path>", methods=["GET", "POST", "DELETE"])
@login_required
def index(path):
    if request.method == "GET":
        return index_get_handler(request, path)

    if request.method == "POST":
        return index_post_handler(request, path)

    if request.method == "DELETE":
        return index_delete_handler(request, path)

    return abort(405)


@views.route("/downloads", defaults={"path": ""}, methods=["GET"])
@views.route("/downloads/<path:path>", methods=["GET"])
@login_required
def download(path):
    if request.method == "GET":
        return download_get_handler(request, path)

    return abort(405)


@views.route("/large-file", defaults={"path": ""}, methods=["GET"])
@login_required
def large_file(path):
    return render_template("large_file.html", user=current_user)


@views.route("/large-file/upload", defaults={"path": ""}, methods=["GET", "POST"])
@login_required
def upload_large_file(path):
    if request.method == "GET":
        return large_file_get_handler(request)

    if request.method == "POST":
        return large_file_post_handler(request)

    return abort(405)
