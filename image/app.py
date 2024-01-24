#!/usr/bin/python3

from flask import Flask, request, jsonify, abort
from werkzeug.utils import secure_filename
from pathlib import Path
from recipes import database as recipes_db
from recipes import blueprint as recipes_bp
import sys

app = Flask(__name__)

def get_api_version():
    return {
        "api_version_major": 0,
        "api_version_minor": 1,
        "api_version_patch": 0,
    }


@app.route('/health', methods=['GET'])
def health():
    return 'OK', 200


@app.route('/version', methods=['GET'])
def version():
    return get_api_version(), 200


if __name__ == '__main__':
    print(f"API version: {get_api_version()}")

    app.config['DATA_FOLDER'] = '/tmp/data'

    if len(sys.argv) == 2:
        app.config['DATA_FOLDER'] = sys.argv[1]

    folder = Path(app.config['DATA_FOLDER'])
    if not folder.exists():
        folder.mkdir(parents=True, exist_ok=True)

    app.config['recipes_db'] = recipes_db.Database(folder / 'recipes.yaml', create_backup=True)

    app.register_blueprint(recipes_bp.RecipesBlueprint, recipes_db=recipes_db)

    app.run(host='0.0.0.0', port=5000)
