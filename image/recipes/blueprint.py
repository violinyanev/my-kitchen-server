#!/usr/bin/python3

from flask import Blueprint

from flask import Flask, request, jsonify, abort, current_app
from werkzeug.utils import secure_filename
from pathlib import Path
from recipes import database as recipe_bp
import sys

RecipesBlueprint = Blueprint('recipes', __name__)


def get_db():
    return current_app.config.get('recipes_db')

@RecipesBlueprint.route('/recipes', methods=['GET'])
def get_recipes():
    return  get_db().get(), 200


@RecipesBlueprint.route('/recipes', methods=['POST'])
def create_recipe():
    data = request.get_json()

    try:
        result, error = get_db().put(data)
        if result:
            return jsonify({"message": "Recipe created successfully", "recipe": result}), 201
        else:
            abort(400, error)
    except:
        abort(400, "Unknown error")


@RecipesBlueprint.route('/recipes/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    success, result = get_db().delete(recipe_id)
    if success:
        return jsonify({"message": "Recipe deleted successfully", "recipe": result}), 204
    else:
        abort(400, result)
