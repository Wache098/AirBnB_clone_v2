#!/usr/bin/python3
"""Defines the DBStorage engine."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os
from models.base_model import Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

class DBStorage:
    """Database storage engine for MySQL"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize the engine and session."""
        user = os.getenv('HBNB_MYSQL_USER')
        password = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        database = os.getenv('HBNB_MYSQL_DB')
        env = os.getenv('HBNB_ENV')

        self.__engine = create_engine(f'mysql+mysqldb://{user}:{password}@{host}/{database}', pool_pre_ping=True)

        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the current database session."""
        obj_dict = {}
        if cls:
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = f'{type(obj).__name__}.{obj.id}'
                obj_dict[key] = obj
        else:
            for cls in [User, Place, State, City, Amenity, Review]:
                objs = self.__session.query(cls).all()
                for obj in objs:
                    key = f'{type(obj).__name__}.{obj.id}'
                    obj_dict[key] = obj
        return obj_dict

    def new(self, obj):
        """Add the object to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None."""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Reload data from the database."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Close the current session."""
        self.__session.remove()

