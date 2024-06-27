#!/usr/bin/python3
"""
Contains the FileStorage class
"""

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {
    "Amenity": Amenity,
    "BaseModel": BaseModel,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User,
}


class FileStorage:
    """serializes instances to a JSON file & deserializes back to instances"""

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """returns the dictionary __objects"""
        if cls:
            if isinstance(cls, str):
                cls = classes.get(cls, None)
            if cls:
                return {k: v for k, v in self.__objects.items() if isinstance(v, cls)}
            return {}
        return self.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        if obj:
            key = f"{obj.__class__.__name__}.{obj.id}"
            self.__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        with open(self.__file_path, "w") as f:
            json.dump({k: v.to_dict() for k, v in self.__objects.items()}, f)

    def reload(self):
        """deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, "r") as f:
                obj_dict = json.load(f)

            for key, value in obj_dict.items():
                cls_name = value['__class__']
                cls = classes[cls_name]
                self.__objects[key] = cls(**value)
        except FileNotFoundError:
            self.__objects = {}
        except Exception as e:
            print(f"Error loading JSON: {e}")


    def delete(self, obj=None):
        """delete obj from __objects if it's inside"""
        if obj:
            key = f"{obj.__class__.__name__}.{obj.id}"
            self.__objects.pop(key, None)

    def close(self):
        """call reload() method for deserializing the JSON file to objects"""
        self.reload()
