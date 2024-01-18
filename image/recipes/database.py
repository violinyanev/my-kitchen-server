#!/usr/bin/env python3

import yaml
import jsonschema
import time

RECIPE_SCHEMA = {
    'type': 'object',
    'properties': {
        'recipes': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'title': {'type': 'string'},
                    'body': {'type': 'string'},
                    'timestamp': {'type': 'integer'},
                    'user': {'type': 'string'},
                },
                'additionalProperties': False,
                'required': [ 'id', 'title', 'timestamp', 'user' ]
            },
        },
    },
    'additionalProperties': False,
}

empty = {
    'recipes': [
    ]
}

class Database:
    def __init__(self, file):
        self.file = file
        if not file.exists():
            with file.open(mode='w') as f:
                f.write(yaml.safe_dump(empty))

        with open(self.file, 'r') as f:
            self.data = yaml.safe_load(f)

        jsonschema.validate(self.data, RECIPE_SCHEMA)


        # TODO: find a better way to handle the IDs
        if self.data['recipes']:
            self.next_id = int(max(self.data['recipes'], key=lambda d: d['id'])['id']) + 1
        else:
            self.next_id = 1


    def get(self):
        return self.data['recipes']


    def put(self, recipe):
        new_recipe = {
            "user": 'Violin', # Fix this
        }

        if 'timestamp' in recipe:
            timestamp = recipe['timestamp']
            if not isinstance(provided_timestamp, int):
                return None, f"timestamp must be of type integer, found '{timestamp}' instead!"
        else:
            timestamp = time.time()

        new_recipe['timestamp'] = timestamp

        if 'id' in recipe:
            provided_id = recipe['id']
            if not isinstance(provided_id, int):
                return None, f"id must be of type integer, found '{provided_id}' instead!"

            if [r for r in self.data['recipes'] if r['id'] == provided_id]:
                return None, f"Recipe with id {recipe['id']} exists!"
            new_recipe['id'] = recipe['id']
        else:
            new_recipe['id'] = self.next_id
            self.next_id += 1


        if 'title' not in recipe or len(recipe['title'].strip()) == 0:
            return None, "Recipe title can't be empty"
        new_recipe['title'] = recipe['title']
        new_recipe['body'] = recipe.get('body', "")

        # TODO don't validate the entire array, just the recipe
        jsonschema.validate(self.data, RECIPE_SCHEMA)

        self.data['recipes'].append(new_recipe)
        self.save()

        return new_recipe, None


    def delete(self, recipe_id):
        for i, r in enumerate(self.data['recipes']):
            if r['id'] == recipe_id:
                deletedRecipe = self.data['recipes'].pop(i)
                self.save()
                return True, deletedRecipe

        return False, f"There is no recipe with id {recipe_id}"


    def save(self):
        with open(self.file, 'w') as f:
            f.write(yaml.safe_dump(self.data))

