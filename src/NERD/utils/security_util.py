import os

from flask import current_app, flash
from NERD import config
from werkzeug.utils import secure_filename


def security(name, rel_path):
    storage_path = current_app.config["STORAGE_PATH"]

    if not sanity_check(name):
        flash(config.SECURITY_ALERT)
        return (False, None)

    sanitized_name = secure_filename(name)
    abs_path = os.path.join(storage_path, rel_path, sanitized_name)

    if not prefix_check(abs_path):
        flash(config.SECURITY_ALERT)
        return (False, None)

    return True, abs_path


def sanity_check(name):
    if not name or name.isspace():
        return False

    if name == "." or ".." in name or "./" in name:
        return False

    if "/" in name:
        if len(name) >= 2 and name.count("/") == 1 and name[-1] == "/":
            return True

        return False

    return True


def prefix_check(path):
    storage_path = current_app.config["STORAGE_PATH"]

    norm_path = os.path.normpath(path)
    real_path = os.path.realpath(norm_path)

    if os.path.commonprefix([storage_path, real_path]) != storage_path:
        return False

    if len(real_path.split("/")) <= len(storage_path.split("/")):
        return False

    return True


def get_hashed_pw():
    base_path = os.path.dirname(__file__)
    hash_path = "/".join(base_path.split("/")[:-1]) + "/hash/hash.txt"

    try:
        with open(hash_path, "r") as f:
            password = f.readline()
    except FileNotFoundError:
        print(
            "Run hash.py to set the login password.\n"
            "Documentation: https://github.com/0xHaru/Nerd-Storage#configuration"
        )
        exit(1)

    return password
