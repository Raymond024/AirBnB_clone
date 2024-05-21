#!/usr/bin/python3
import unittest
import os
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.engine.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):
    def setUp(self):
        self.storage = FileStorage()
        self.storage.reload()

    def test_attributes(self):
        self.assertTrue(hasattr(self.storage, "_FileStorage__file_path"))
        self.assertTrue(hasattr(self.storage, "_FileStorage__objects"))

    def test_all_method(self):
        all_objects = self.storage.all()
        self.assertIsInstance(all_objects, dict)
        self.assertEqual(all_objects, self.storage._FileStorage__objects)

    def test_new_method(self):
        new_obj = BaseModel()
        self.storage.new(new_obj)
        key = "{}.{}".format(new_obj.__class__.__name__, new_obj.id)
        self.assertIn(key, self.storage._FileStorage__objects)
        self.assertEqual(self.storage._FileStorage__objects[key], new_obj)

    def test_save_method(self):
        new_obj = BaseModel()
        self.storage.new(new_obj)
        self.storage.save()
        filename = self.storage._FileStorage__file_path
        with open(filename, 'r') as f:
            data = f.read()
            self.assertIn(new_obj.__class__.__name__, data)
            self.assertIn(new_obj.id, data)

    def test_reload_method(self):
        new_obj = BaseModel()
        self.storage.new(new_obj)
        self.storage.save()
        self.storage.reload()
        key = "{}.{}".format(new_obj.__class__.__name__, new_obj.id)
        self.assertIn(key, self.storage._FileStorage__objects)

    def tearDown(self):
        filename = self.storage._FileStorage__file_path
        try:
            os.remove(filename)
        except FileNotFoundError:
            pass


if __name__ == '__main__':
