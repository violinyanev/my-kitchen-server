#!/usr/bin/env python3

import yaml
import jsonschema

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
                    'date': {'type': 'string'},
                    'user': {'type': 'string'},
                },
                'additionalProperties': False,
                'required': [ 'id', 'title', 'date', 'user' ]
            },
        },
    },
    'additionalProperties': False,
}

empty = {
    'recipes': [
    ]
}

RECIPE_DATE_FORMAT = '%Y-%m-%d-%H-%M'


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
        return self.data


    def put(self, recipe):
        if 'title' not in recipe or len(recipe['title'].strip()) == 0:
            raise "Recipe title can't be empty"
        new_recipe = {
            "id": self.next_id,
            "title": recipe['title'],
            "body": recipe['body'],
            "date": '2024-01-15-16-04', # Fix this
            "user": 'Violin', # Fix this
        }
        self.next_id += 1

        jsonschema.validate(self.data, RECIPE_SCHEMA)

        self.data['recipes'].append(new_recipe)

        with open(self.file, 'w') as f:
            f.write(yaml.safe_dump(self.data))
