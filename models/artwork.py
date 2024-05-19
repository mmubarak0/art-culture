#!/usr/bin/python
"""Artwork table"""
import models
import sqlalchemy
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship

like_artwork = Table(
                "like_artwork",
                Base.metadata,
                Column('artist_id', String(60), ForeignKey('artists.id')),
                Column('artwork_id', String(60), ForeignKey('artworks.id'))
            )


class Artwork(BaseModel, Base):
    """Artwork columns."""
    __tablename__ = 'artworks'
    artist_id = Column(String(60), ForeignKey('artists.id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(String(5000))
    views = Column(Integer, default=0)
    order = Column(Integer, default=0)
    comments = relationship('Comment', backref="artwork")
    likes = relationship(
                'Artist', secondary=like_artwork, backref="liked_artworks"
            )

    def __repr__(self):
        return f"({self.id}) title='{self.title}'"

    def __init__(self, *args, **kwargs):
        """initializes artwork"""
        super().__init__(*args, **kwargs)
