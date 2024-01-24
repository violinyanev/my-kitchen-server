#!/usr/bin/python3

from flask import Blueprint

from flask import Flask, request, jsonify, abort, current_app
from werkzeug.utils import secure_filename
from pathlib import Path
from users import database as users_bp
import sys

UsersBlueprint = Blueprint('users', __name__)


def get_db():
    return current_app.config.get('users_db')

@UsersBlueprint.route('/users', methods=['GET'])
def get_recipes():
    return  get_db().get(), 200

