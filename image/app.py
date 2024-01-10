#!/usr/bin/python3

from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from pathlib import Path
from recipes import database as recipe_db
import sys

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_api_version():
    return {
        "api_version_major": 0,
        "api_version_minor": 1,
        "api_version_patch": 0,
    }


@app.route('/health', methods=['GET'])
def health():
    return 'OK', 200



@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    # If the user does not select a file, the browser submits an empty file without a filename
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = Path(app.config['UPLOAD_FOLDER']) / filename
        file.save(filepath)
        return jsonify({'message': 'File uploaded successfully', 'filename': filename})
    else:
        return jsonify({'error': 'Invalid file format'})


@app.route('/albums', methods=['GET'])
def albums():
    # Set the upload folder

    if directory.is_dir():
        albums = {
            **get_api_version(),
            "albums": []
        }

        for item in directory.iterdir():
            if item.is_file():
                #content += (f"File: {item.name}\n")
                pass
            elif item.is_dir():
                albums['albums'].append(item.name)

        return albums, 200
    else:
        print("Bad data directory")
        return 'No data', 404



@app.route('/recipes', methods=['GET'])
def recipes():
    return {
        **get_api_version(),
        **recipe_db.get()
    }, 200


if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = '/tmp/data'
    if len(sys.argv) == 2:
        app.config['UPLOAD_FOLDER'] = sys.argv[1]

    folder = Path(app.config['UPLOAD_FOLDER'])
    if not folder.exists():
        folder.mkdir(parents=True, exist_ok=True)
    app.run(host='0.0.0.0', port=5000)
