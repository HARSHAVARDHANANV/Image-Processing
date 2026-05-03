from flask import Flask, render_template, request, jsonify, send_from_directory, session, url_for
import os
import time
import cv2
import numpy as np
from werkzeug.utils import secure_filename

# Application folders and allowed image extensions
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER
app.secret_key = "replace-this-with-a-secure-key"

# Make sure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def allowed_file(filename):
    """Check that the uploaded file has an allowed image extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    """Render the main page."""
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_image():
    """Handle image uploads and save them to the uploads folder."""
    if "image" not in request.files:
        return jsonify({"error": "No file part in the request."}), 400

    image_file = request.files["image"]
    if image_file.filename == "":
        return jsonify({"error": "No file selected."}), 400

    if not allowed_file(image_file.filename):
        return jsonify({"error": "Invalid file type. Use jpg, jpeg, or png."}), 400

    filename = secure_filename(image_file.filename)
    timestamp = int(time.time() * 1000)
    saved_filename = f"{timestamp}_{filename}"
    saved_path = os.path.join(app.config["UPLOAD_FOLDER"], saved_filename)

    image_file.save(saved_path)
    session["uploaded_image"] = saved_filename
    session["current_image"] = saved_filename

    return jsonify({
        "message": "Image uploaded successfully.",
        "image_url": url_for("uploaded_file", filename=saved_filename),
    })


def get_current_image_path():
    """Get the last image path from session, preferring processed output first."""
    filename = session.get("current_image") or session.get("uploaded_image")
    if not filename:
        return None

    for folder in (app.config["OUTPUT_FOLDER"], app.config["UPLOAD_FOLDER"]):
        possible_path = os.path.join(folder, filename)
        if os.path.exists(possible_path):
            return possible_path
    return None


@app.route("/process/<filter_name>", methods=["POST"])
def process_image(filter_name):
    """Apply a selected filter to the latest image in session."""
    input_path = get_current_image_path()
    if not input_path:
        return jsonify({"error": "Please upload an image before applying a filter."}), 400

    image = cv2.imread(input_path)
    if image is None:
        return jsonify({"error": "Failed to read the current image."}), 400

    processed = apply_filter(image, filter_name)
    if processed is None:
        return jsonify({"error": "Unknown filter selected."}), 400

    output_filename = f"processed_{filter_name}_{int(time.time() * 1000)}.jpg"
    output_path = os.path.join(app.config["OUTPUT_FOLDER"], output_filename)
    cv2.imwrite(output_path, processed)
    session["current_image"] = output_filename

    return jsonify({
        "message": "Filter applied successfully.",
        "output_url": url_for("output_file", filename=output_filename),
        "output_filename": output_filename,
    })


@app.route("/adjust", methods=["POST"])
def adjust_image():
    """Adjust brightness and contrast on the latest image."""
    input_path = get_current_image_path()
    if not input_path:
        return jsonify({"error": "Please upload an image before adjusting brightness and contrast."}), 400

    image = cv2.imread(input_path)
    if image is None:
        return jsonify({"error": "Failed to read the current image."}), 400

    try:
        brightness = int(request.form.get("brightness", 0))
        contrast = float(request.form.get("contrast", 1.0))
    except ValueError:
        return jsonify({"error": "Invalid brightness or contrast value."}), 400

    processed = apply_brightness_contrast(image, brightness, contrast)
    output_filename = f"processed_brightness_contrast_{int(time.time() * 1000)}.jpg"
    output_path = os.path.join(app.config["OUTPUT_FOLDER"], output_filename)
    cv2.imwrite(output_path, processed)
    session["current_image"] = output_filename

    return jsonify({
        "message": "Brightness and contrast adjusted successfully.",
        "output_url": url_for("output_file", filename=output_filename),
        "output_filename": output_filename,
    })


@app.route("/reset", methods=["POST"])
def reset_image():
    """Reset the session to the original uploaded image."""
    uploaded_filename = session.get("uploaded_image")
    if not uploaded_filename:
        return jsonify({"error": "No uploaded image to reset."}), 400

    session["current_image"] = uploaded_filename
    return jsonify({"message": "Image reset to original."})


def apply_brightness_contrast(image, brightness=0, contrast=1.0):
    """Apply OpenCV brightness and contrast adjustment."""
    return cv2.convertScaleAbs(image, alpha=contrast, beta=brightness)


def apply_filter(image, filter_name):
    """Apply one of the supported filters using OpenCV."""
    lower_name = filter_name.lower()

    if lower_name == "grayscale":
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if lower_name == "edge":
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return cv2.Canny(gray, 100, 200)

    if lower_name == "blur":
        return cv2.GaussianBlur(image, (15, 15), 0)

    if lower_name == "flip":
        return cv2.flip(image, 1)

    if lower_name == "threshold":
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
        return binary

    if lower_name == "sharpen":
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], dtype=np.float32)
        return cv2.filter2D(image, -1, kernel)

    if lower_name == "sepia":
        sepia_kernel = np.array([
            [0.272, 0.534, 0.131],
            [0.349, 0.686, 0.168],
            [0.393, 0.769, 0.189],
        ], dtype=np.float32)
        sepia = cv2.transform(image, sepia_kernel)
        sepia = np.clip(sepia, 0, 255).astype("uint8")
        return sepia

    return None


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    """Send uploaded image files for preview."""
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/outputs/<filename>")
def output_file(filename):
    """Send processed image files for preview and download."""
    return send_from_directory(app.config["OUTPUT_FOLDER"], filename)


if __name__ == "__main__":
    app.run(debug=True)
