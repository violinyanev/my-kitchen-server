#!/usr/bin/env python3

import yaml
import jsonschema
import time
import shutil
from datetime import datetime
from pathlib import Path

USERS_SCHEMA = {
    'type': 'object',
    'properties': {
        'users': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'password': {'type': 'string'},
                    'name': {'type': 'string'},
                    'email': {'type': 'string'},
                },
                'additionalProperties': False,
                'required': [ 'name', 'password', 'email' ]
            },
        },
    },
    'additionalProperties': False,
}

empty = {
    'users': [
    ]
}

class Database:
    def __init__(self, file, create_backup = False):
        self.file = file
        if not file.exists():
            with file.open(mode='w') as f:
                f.write(yaml.safe_dump(empty))
        elif create_backup:
            backup_directory = file.parent / "backup"
            date = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M')
            backup_file = backup_directory / (file.stem + "-" + date + ".yaml")
            backup_directory.mkdir(exist_ok=True)
            shutil.copy(file, backup_file)

        with open(self.file, 'r') as f:
            self.data = yaml.safe_load(f)

        try:
            jsonschema.validate(self.data, USERS_SCHEMA)
        except:
            # TODO implement conversion scripts or use a proper DB
            print("Found database file can not be validated! Creating a backup and a new database")
            backup_directory = file.parent / "backup"
            date = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M')
            backup_file = backup_directory / (file.stem + "-incompatible-" + date + ".yaml")
            backup_directory.mkdir(exist_ok=True)
            shutil.copy(file, backup_file)
            with file.open(mode='w') as f:
                f.write(yaml.safe_dump(empty))
            with open(self.file, 'r') as f:
                self.data = yaml.safe_load(f)


    def get(self):
        return self.data['users']

