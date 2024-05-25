#!/usr/bin/python3
"""Category Table"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Table, ForeignKey
from sqlalchemy.orm import relationship

artwork_category_relation = Table(
        'artwork_category_relation',
        Base.metadata,
        Column('artwork_id', String(60), ForeignKey('artworks.id')),
        Column('category_id', String(60), ForeignKey('categories.id'))
)


class Category(BaseModel, Base):
    """Category columns"""
    __tablename__ = 'categories'
    name = Column(String(128), nullable=False)
    artworks = relationship("Artwork", secondary=artwork_category_relation,
                            backref="categories")

    def __repr__(self):
        return f"{self.id} name='{self.name}'"

    def __init__(self, *args, **kwargs):
        """initializes category"""
        super().__init__(*args, **kwargs)
