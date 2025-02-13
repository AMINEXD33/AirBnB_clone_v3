#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import hashlib


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        if (kwargs.get("password")):
            kwargs["password"] = self.get_me_hashed_md5(kwargs.get("password"))
        super().__init__(*args, **kwargs)

    def get_me_hashed_md5(self, value):
        """hash a value to md5 and return it's value"""
        hashed = hashlib.md5()
        hashed.update(value.encode("utf-8"))
        hashed = hashed.hexdigest()
        return hashed
