from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash

from .models import User

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User()

        input_password = request.form.get("password")

        if check_password_hash(user.password, input_password):
            login_user(user, remember=True)
            return redirect(url_for("views.index"))
        else:
            flash("Incorrect password.")

    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
