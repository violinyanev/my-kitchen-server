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

    def get(self):
        return self.data


    def put(self, recipe):
        pass
