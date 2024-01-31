#!/usr/bin/python3
"""Comment Table"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Comment(BaseModel, Base):
    """Comment columns"""
    __tablename__ = 'comments'
    artist_id = Column(String(60), ForeignKey('artists.id'), nullable=False)
    artwork_id = Column(String(60), ForeignKey('artworks.id'), nullable=False)
    content = Column(String(5000), nullable=False)

    def __repr__(self):
        return f"{self.id} content={self.content}"

    def __init__(self, *args, **kwargs):
        """initializes comment"""
        super().__init__(*args, **kwargs)
