# Import relevant libraries and modules
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    send_from_directory,
)
from werkzeug.utils import secure_filename
import os
from os.path import join, splitext, exists, getmtime
from os import urandom, listdir

app = Flask(__name__)

app.secret_key = urandom(24)

# Set the folder where images are stored
# Use /pictures for production (container), uploads for local dev
app.config["UPLOAD_FOLDER"] = os.getenv("PICTURES_DIR", "uploads")

# Ensure upload folder exists
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

IMG_EXTENSIONS = {".svg", ".png", ".jpg", ".jpeg", ".gif"}


def is_img_file(fname):
    """Check if filename has a valid image extension."""
    _, extension = splitext(fname)
    return extension.lower() in IMG_EXTENSIONS


def get_images():
    """
    Get list of images from the upload folder.
    Returns list of dicts with file_name and mtime (modification time).
    """
    upload_folder = app.config["UPLOAD_FOLDER"]

    if not exists(upload_folder):
        return []

    images = []
    for filename in listdir(upload_folder):
        if is_img_file(filename):
            file_path = join(upload_folder, filename)
            try:
                mtime = getmtime(file_path)
                images.append({
                    "file_name": filename,
                    "mtime": mtime
                })
            except OSError:
                # Skip files that can't be accessed
                continue

    # Sort by modification time (newest first)
    images.sort(key=lambda x: x["mtime"], reverse=True)

    return images


# Define route for the index (home) page, accepting only GET method
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", images=get_images())


# Define route with accepted methods GET and POST
@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    # Check if the method of the request is POST (form data submission)
    if request.method == "POST":
        if "file" not in request.files:
            print("no file in request")
            return redirect(request.url)  # Redirect user back to the form page

        file = request.files["file"]

        if file.filename == '' or not is_img_file(file.filename):
            return render_template("message.html", message="No valid image file provided")

        fname = secure_filename(file.filename)
        file_path = join(app.config["UPLOAD_FOLDER"], fname)

        # Save the file to the specified directory
        file.save(file_path)

        # Redirect to the home page after upload is successful
        return redirect("/")

    # If the method of the request is GET, show an upload form to the user
    return render_template("message.html", message="Upload your photos.")


# Define route for the preview page that accepts a dynamic 'name' parameter in the URL
@app.route("/preview/<imgname>")
def preview(imgname):
    return render_template("preview.html", name=imgname)


# Assuming 'preview' end-point exists to show the uploaded image to the user
@app.route("/download/<imgname>")
def download(imgname):
    return send_from_directory(app.config["UPLOAD_FOLDER"], imgname, as_attachment=True)


# Define a route to serve static files. For example, images, CSS, JavaScript, etc.
@app.route("/static/<name>")
def get_static(name):
    return send_from_directory("static", name)


# To keep the application running
if __name__ == "__main__":
    app.run(debug=True, port=5001, host='0.0.0.0')
