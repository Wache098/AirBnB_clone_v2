#!/usr/bin/python3
""" State module """
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models.city import City
import models

class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state", cascade="all, delete")

    @property
    def cities(self):
        """ Getter attribute to return list of City instances with state_id """
        city_list = []
        all_cities = models.storage.all(City)
        for city in all_cities.values():
            if city.state_id == self.id:
                city_list.append(city)
        return city_list
