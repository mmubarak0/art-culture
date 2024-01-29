#!/usr/bin/python3
"""Message Table"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Message(BaseModel, Base):
    """Message columns"""
    __tablename__ = 'messages'
    sender_id = Column(String(60), ForeignKey('artists.id'), nullable=False)
    receiver_id = Column(String(60), ForeignKey('artists.id'), nullable=False)
    content = Column(String(5000), nullable=False)

    def __init__(self, *args, **kwargs):
        """initializes message"""
        super().__init__(*args, **kwargs)

