#!/usr/bin/env python3

import unittest
from pathlib import Path
import jsonschema
import yaml
from recipes import database

class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.test_file = Path("test_database.yaml")

    def tearDown(self):
        if self.test_file.exists():
            self.test_file.unlink()

    def test_init(self):
        db = database.Database(self.test_file)
        self.assertTrue(self.test_file.exists())
        self.assertEqual(db.data, {'recipes': []})
        self.assertEqual(db.next_id, 1)
        self.assertEqual(db.get(), [])

    def test_put_valid_recipe(self):
        db = database.Database(self.test_file)
        recipe = {"id": 1, "title": "Test Recipe", "body": "Recipe body", "timestamp": 12}
        new_recipe, error = db.put(recipe)
        self.assertIsNone(error)
        self.assertIn(new_recipe, db.data['recipes'])
        self.assertEqual(new_recipe['timestamp'], 12)

    def test_put_id_not_int(self):
        db = database.Database(self.test_file)
        recipe = {"id": "not an integer", "title": "Test Recipe", "body": "Recipe body"}
        new_recipe, error = db.put(recipe)
        self.assertEqual(error, "id must be of type integer, found 'not an integer' instead!")
        self.assertNotIn(new_recipe, db.data['recipes'])

    def test_put_id_null(self):
        db = database.Database(self.test_file)
        recipe = {"id": None, "title": "Test Recipe", "body": "Recipe body"}
        new_recipe, error = db.put(recipe)
        self.assertEqual(error, "id must be of type integer, found 'None' instead!")
        self.assertNotIn(new_recipe, db.data['recipes'])

    def test_put_existing_id(self):
        db = database.Database(self.test_file)
        recipe = {"id": 1, "title": "Test Recipe", "body": "Recipe body"}
        db.put(recipe)
        result, error = db.put(recipe)
        self.assertEqual(error, "Recipe with id 1 exists!")
        self.assertIsNone(result)

    def test_put_timestamp_not_int(self):
        db = database.Database(self.test_file)
        recipe = {"id": 1, "title": "Test Recipe", "body": "Recipe body", "timestamp": "not int"}
        db.put(recipe)
        result, error = db.put(recipe)
        self.assertEqual(error, "timestamp must be of type integer, found 'not int' instead!")
        self.assertIsNone(result)

    def test_put_empty_title(self):
        db = database.Database(self.test_file)
        recipe = {"id": 1, "title": "", "body": "Recipe body"}
        result, error = db.put(recipe)
        self.assertEqual(error, "Recipe title can't be empty")
        self.assertIsNone(result)

    def test_delete_existing_recipe(self):
        db = database.Database(self.test_file)
        recipe = {"id": 1, "title": "Test Recipe", "body": "Recipe body"}
        recipe,_ = db.put(recipe)
        success, deleted_recipe = db.delete(1)
        self.assertTrue(success)
        self.assertEqual(deleted_recipe, recipe)
        self.assertNotIn(recipe, db.data['recipes'])

    def test_delete_nonexistent_recipe(self):
        db = database.Database(self.test_file)
        success, error = db.delete(1)
        self.assertFalse(success)
        self.assertEqual(error, "There is no recipe with id 1")

    def test_save(self):
        db = database.Database(self.test_file)
        recipe = {"id": 1, "title": "Test Recipe", "body": "Recipe body"}
        db.put(recipe)
        db.save()
        with self.test_file.open('r') as f:
            saved_data = yaml.safe_load(f)
        self.assertEqual(saved_data, db.data)


if __name__ == '__main__':
    unittest.main()
