#!/usr/bin/python3

from flask import Flask
from pathlib import Path

app = Flask(__name__)


@app.route('/health', methods=['GET'])
def health():
    return 'OK', 200


@app.route('/albums', methods=['GET'])
def albums():
    directory = Path('/var/data') # TODO make configurable

    if directory.is_dir():
        albums = {
            "api_version_major": 0,
            "api_version_minor": 1,
            "api_version_patch": 0,
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



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
