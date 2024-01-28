#!/usr/bin/python
"""Artwork table"""
import models
import sqlalchemy
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Artwork(BaseModel, Base):
    """Artwork columns."""
    __tablename__ = 'artworks'
    artist_id = Column(String(60), ForeignKey('artists.id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(String(5000))

    def __init__(self, *args, **kwargs):
        """initializes artwork"""
        super().__init__(*args, **kwargs)
