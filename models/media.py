#!/usr/bin/python3
"""Media Table"""
import models
import sqlalchemy
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship


class Media(BaseModel, Base):
    """Media columns"""

    __tablename__ = "medias"
    artwork_id = Column(String(60), ForeignKey("artworks.id"), nullable=False)
    url = Column(String(550), nullable=False)
    type = Column(String(550), nullable=False)
    name = Column(String(256))

    def __repr__(self):
        return f"{self.id} url={self.url}"

    def __init__(self, *args, **kwargs):
        """initializes media"""
        super().__init__(*args, **kwargs)
