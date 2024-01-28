#!/usr/bin/python3
"""Artist Table"""
import models
import sqlalchemy
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Artist(BaseModel, Base):
    """Artist columns"""
    __tablename__ = 'artists'
    # email instead of (username) as better unique identfier.
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    artworks = relationship("Artwork", backref="artist")

    def __init__(self, *args, **kwargs):
        """initializes artist"""
        super().__init__(*args, **kwargs)
