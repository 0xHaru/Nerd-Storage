import os
import shutil
import zipfile
from pathlib import Path

from flask import (
    Response,
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    send_file,
)
from flask_login import current_user

from .utils.security_util import prefix_check, security
from .utils.util import (
    RemoveFile,
    exist_check,
    merge_chunks,
    replace_dir,
    sort_index,
    unzip,
    zip_directory,
)


# /index
# Method: GET
def index_get_handler(request, path):
    storage_path = current_app.config["STORAGE_PATH"]
    abs_path = os.path.join(storage_path, path)

    if abs_path != f"{storage_path}/" and not prefix_check(abs_path):
        return Response(status=400)

    if not os.path.exists(abs_path):
        return abort(404)

    if os.path.isfile(abs_path):
        return send_file(abs_path)

    # { 'filename': '/index/.../filename', ..., 'dir_name': '/index/.../dir_name', ... }
    index = dict([(x, os.path.join(request.path, x)) for x in os.listdir(abs_path)])
    sorted_index = sort_index(index, request.path)

    directory = "/" if not path else path.split("/")[-1]

    return render_template(
        "index.html", user=current_user, directory=directory, index=sorted_index
    )


# Method: POST
def index_post_handler(request, path):
    storage_path = current_app.config["STORAGE_PATH"]
    rel_path = path

    if request.form:
        keys = list(request.form.keys())

        # Create a directory
        if "directory" in keys:
            dir_name = request.form.get("directory")
            safe, abs_path = security(dir_name, rel_path)

            if not safe:
                return redirect(request.referrer)

            if exist_check(dir_name, abs_path, "post"):
                return redirect(request.referrer)

            os.mkdir(abs_path)

            return redirect(request.referrer)

        # Update a file / directory
        if "updated-name" in keys:
            dir_flag = 0
            original_name = request.form.get("original-name")
            updated_name = request.form.get("updated-name")

            # If it's a directory
            if original_name[-1] == "/":
                dir_flag = 1
                safe, new_abs_path = security(updated_name, rel_path)
            else:
                safe, new_abs_path = security(updated_name, rel_path)

            if not safe:
                return redirect(request.referrer)

            abs_path = os.path.join(storage_path, rel_path, original_name)
            f = request.files["updated-file"]

            if f:
                if dir_flag:
                    replace_dir(f, abs_path, new_abs_path)
                else:
                    f.save(new_abs_path)
            elif abs_path != new_abs_path:
                os.rename(abs_path, new_abs_path)

            return redirect(request.referrer)

    # Upload file / directory (.zip file)
    if request.files:
        files = request.files.getlist("file")
        dir_checkbox = bool(request.form.get("dir-checkbox"))

        for f in files:
            zip_flag = 0
            filename = f.filename

            if dir_checkbox and zipfile.is_zipfile(f):
                zip_flag = 1
                filename = str(Path(filename).with_suffix(""))

            # Move pointer back to the beginning of the file
            f.stream.seek(0)

            safe, abs_path = security(filename, rel_path)

            if not safe:
                return redirect(request.referrer)

            if exist_check(filename, abs_path, "post"):
                return redirect(request.referrer)

            if zip_flag:
                abs_path = "/".join(abs_path.split("/")[:-1])
                unzip(f, abs_path)
            else:
                f.save(abs_path)

        return redirect(request.referrer)


# Method: DELETE
def index_delete_handler(request, path):
    status = 500

    # If it's a directory
    if path[-1] == "/":
        res_name = path.split("/")[-2]
        rel_path = "/".join(path.split("/")[:-2])
    else:
        res_name = path.split("/")[-1]
        rel_path = "/".join(path.split("/")[:-1])

    safe, abs_path = security(res_name, rel_path)

    if not safe:
        status = 400
        return Response(status=status)

    if exist_check(res_name, abs_path, "delete"):
        status = 400
        return Response(status=status)

    if os.path.isfile(abs_path):
        os.remove(abs_path)
        status = 200
    elif os.path.isdir(abs_path):
        shutil.rmtree(abs_path)
        status = 200

    return Response(status=status)


# /downloads
# Method: GET
def download_get_handler(request, path):
    storage_path = current_app.config["STORAGE_PATH"]
    abs_path = os.path.join(storage_path, path)

    if abs_path != f"{storage_path}/" and not prefix_check(abs_path):
        return Response(status=400)

    if not os.path.exists(abs_path):
        return abort(404)

    if os.path.isfile(abs_path):
        return send_file(abs_path, as_attachment=True)

    if os.path.isdir(abs_path):
        if not os.listdir(abs_path):
            flash("Empty directory.")
            return redirect(request.referrer)

        dir_name = abs_path.split("/")[-1]
        zipped = zip_directory(abs_path)

        # Remove temp archive
        thread = RemoveFile(zipped)
        thread.start()

        return send_file(
            zipped,
            mimetype="application/zip",
            as_attachment=True,
            download_name=f"{dir_name}.zip",
        )


# /large-file/upload
# Method: GET
def large_file_get_handler(request):
    tmp_path = f"{current_app.config['BASE_PATH']}/tmp"

    chunk_number = request.args.get("flowChunkNumber", type=int)
    filename = request.args.get("flowFilename", type=str)
    identifier = request.args.get("flowIdentifier", type=str)
    identifier = identifier.split("-")[0]

    path = f"{tmp_path}/{identifier}"

    chunk_name = f"{chunk_number}_{filename}"
    chunk_path = f"{path}/{chunk_name}"

    if os.path.isfile(chunk_path):
        # This chunk already exists
        return Response(status=200)
    else:
        # This chunk does not exists and needs to be uploaded
        return Response(status=100)


# /large-file/upload
# Method: POST
def large_file_post_handler(request):
    tmp_path = f"{current_app.config['BASE_PATH']}/tmp"

    total_chunks = request.form.get("flowTotalChunks", type=int)
    chunk_number = request.form.get("flowChunkNumber", default=1, type=int)
    filename = request.form.get("flowFilename", default="error", type=str)
    identifier = request.form.get("flowIdentifier", default="error", type=str)
    identifier = identifier.split("-")[0]

    # Get the chunk
    chunk = request.files["file"]

    path = f"{tmp_path}/{identifier}"

    if not os.path.isdir(path):
        os.mkdir(path)

    # Save the chunk
    chunk_name = f"{chunk_number}_{filename}"
    chunk_path = f"{path}/{chunk_name}"
    chunk.save(chunk_path)

    if chunk_number == total_chunks:
        merge_chunks(path, filename)
        shutil.rmtree(path)

    return Response(status=200)
