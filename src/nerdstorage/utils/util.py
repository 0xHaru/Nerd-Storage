import glob
import os
import shutil
import time
import uuid
import zipfile
from collections import OrderedDict
from pathlib import Path
from threading import Thread

from flask import current_app, flash


def sort_index(index, path):
    sorted_index = OrderedDict()
    dirs = []
    files = []

    storage_path = current_app.config["STORAGE_PATH"]
    split_path = path.split("/")

    if len(split_path) > 2:
        sorted_index[".."] = "/".join(split_path[:-1])
    else:
        sorted_index[".."] = "/"

    for key in index.keys():
        ref = "/".join(index[key].split("/")[2:])
        dir_path = os.path.join(storage_path, ref)

        if os.path.isdir(dir_path):
            dirs.append(key)
        else:
            files.append(key)

    for x in sorted(dirs, key=str.lower):
        sorted_index[f"{x}/"] = index[x]

    for x in sorted(files, key=str.lower):
        sorted_index[x] = index[x]

    return sorted_index


def exist_check(name, abs_path, method):
    if method == "post" and os.path.exists(abs_path):
        flash(f"{name} already exists.")
        return True

    if (method == "get" or method == "delete") and not os.path.exists(abs_path):
        flash(f"{name} does not exist.")
        return True

    return False


def replace_dir(f, abs_path, new_abs_path):
    if zipfile.is_zipfile(f):
        shutil.rmtree(abs_path)
        unzipped_path = "/".join(new_abs_path.split("/")[:-1])
        unzip(f, unzipped_path)

        filename = str(Path(f.filename).with_suffix(""))
        unzipped_path = os.path.join(unzipped_path, filename)

        if unzipped_path != new_abs_path:
            os.rename(unzipped_path, new_abs_path)
    else:
        flash("Only .zip files are allowed.")


def zip_directory(path):
    base_path = current_app.config["BASE_PATH"]

    name = uuid.uuid4().hex

    src = f"{os.getcwd()}/{name}.zip"
    dest = f"{base_path}/tmp/{name}.zip"

    shutil.make_archive(name, "zip", path)
    return shutil.move(src, dest)


def unzip(src, dest):
    with zipfile.ZipFile(src, "r") as z:
        z.extractall(dest)


def merge_chunks(path, filename):
    storage_path = current_app.config["STORAGE_PATH"]

    chunks = sorted(
        glob.glob(f"{path}/*"),
        key=lambda x: int(x.rsplit("/")[-1].split("_")[0]),
    )

    with open(f"{storage_path}/{filename}", "wb") as dest:
        for chunk in chunks:
            with open(chunk, "rb") as src:
                shutil.copyfileobj(src, dest)


class RemoveFile(Thread):
    def __init__(self, path):
        Thread.__init__(self)
        self.path = path

    def run(self):
        time.sleep(5)
        os.remove(self.path)
