#!/usr/bin/python3
""" Base model module """
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import models

Base = declarative_base()

class BaseModel:
    """ Base class for all models """
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, *args, **kwargs):
        """ Initialize a new model instance """
        self.id = str(uuid.uuid4())
        self.created_at = self.updated_at = datetime.utcnow()
        for key, value in kwargs.items():
            setattr(self, key, value)

    def save(self):
        """ Save the model instance """
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """ Convert instance to dictionary format """
        my_dict = self.__dict__.copy()
        my_dict["__class__"] = self.__class__.__name__
        my_dict["created_at"] = self.created_at.isoformat()
        my_dict["updated_at"] = self.updated_at.isoformat()
        my_dict.pop("_sa_instance_state", None)
        return my_dict

    def delete(self):
        """ Delete the current instance from storage """
        models.storage.delete(self)

