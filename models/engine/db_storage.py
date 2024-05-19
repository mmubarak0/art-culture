#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
import sqlalchemy
import conf
from models.base_model import BaseModel, Base
from models.artist import Artist
from models.artwork import Artwork
from models.categories import Category
from models.message import Message
from models.comment import Comment
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {
        "Artwork": Artwork, "Artist": Artist,
        "Category": Category, "Message": Message,
        "Comment": Comment
    }


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        ANC_MYSQL_USER = conf.ANC_MYSQL_USER
        ANC_MYSQL_PWD = conf.ANC_MYSQL_PWD
        ANC_MYSQL_HOST = conf.ANC_MYSQL_HOST
        ANC_MYSQL_DB = conf.ANC_MYSQL_DB
        ANC_ENV = conf.ANC_ENV
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(ANC_MYSQL_USER,
                                             ANC_MYSQL_PWD,
                                             ANC_MYSQL_HOST,
                                             ANC_MYSQL_DB))
        if ANC_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """ get the 'cls' object from the storage"""

        for clss in classes.keys():
            if cls == clss or cls is classes[clss]:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    if id == obj.id:
                        return obj
        return None

    def count(self, cls=None):
        """ counts the number of object in the storage"""
        return len(self.all(cls))
