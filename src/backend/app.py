import os
import cv2
import numpy as np
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Flask app initialization
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})  # Allow communication between frontend (port 3001) and backend

# Configure upload and output directories
UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')
PROCESSED_FOLDER = os.path.join(app.root_path, 'processed')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def sharpness_adjustment(image):
    sharpening_kernel = np.array([[0, -1, 0],
                                   [-1, 5, -1],
                                   [0, -1, 0]])
    return cv2.filter2D(image, -1, sharpening_kernel)

def smoothing_denoising(image):
    gaussian_blur = cv2.GaussianBlur(image, (5, 5), 0)
    return cv2.bilateralFilter(gaussian_blur, d=9, sigmaColor=75, sigmaSpace=75)

def contrast_adjustment(image, factor=1.2):
    return cv2.convertScaleAbs(image, alpha=factor, beta=0)

def split_image(image):
    h, w = image.shape[:2]
    mid_h, mid_w = h // 2, w // 2
    return [
        image[:mid_h, :mid_w],  # Top-left
        image[:mid_h, mid_w:],  # Top-right
        image[mid_h:, :mid_w],  # Bottom-left
        image[mid_h:, mid_w:]   # Bottom-right
    ]

@app.route('/process', methods=['POST'])
def process_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save the uploaded file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    print(f"File saved: {file_path}")  # Log the file save

    # Read and process the image
    image = cv2.imread(file_path)
    if image is None:
        return jsonify({"error": "Invalid image file"}), 400

    # Split the image
    parts = split_image(image)
    processed_files = []

    for idx, part in enumerate(parts):
        part = contrast_adjustment(part)
        part = sharpness_adjustment(part)
        part = smoothing_denoising(part)

        # Save the enhanced part
        processed_filename = f"enhanced_part_{idx + 1}.jpg"
        processed_path = os.path.join(PROCESSED_FOLDER, processed_filename)
        cv2.imwrite(processed_path, part)
        print(f"File saved: {processed_path}")  # Log each saved processed file
        processed_files.append(processed_filename)

    return jsonify({"file_names": processed_files}), 200

@app.route('/download/<filename>', methods=['GET'])
def download_image(filename):
    try:
        file_path = os.path.join(PROCESSED_FOLDER, filename)
        if os.path.exists(file_path):
            print(f"File exists: {file_path}")  # Log if file exists
            return send_from_directory(PROCESSED_FOLDER, filename, as_attachment=True)
        else:
            print(f"File not found: {file_path}")  # Log if file is missing
            return jsonify({"error": "File not found"}), 404
    except Exception as e:
        print(f"Error: {e}")  # Log unexpected errors
        return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
