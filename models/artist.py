#!/usr/bin/python3
"""Artist Table"""
import models
import sqlalchemy
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin


class Artist(BaseModel, Base, UserMixin):
    """Artist columns"""
    __tablename__ = 'artists'
    # email instead of (username) as better unique identfier.
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    artworks = relationship("Artwork", backref="artist")
    messages_outbox = relationship(
        "Message", primaryjoin="Artist.id==Message.sender_id", backref="sender"
    )
    messages_inbox = relationship(
        "Message", primaryjoin="Artist.id==Message.receiver_id",
        backref="receiver"
    )
    comments = relationship("Comment", backref="artist")
    following = relationship(
        'Artist', lambda: artist_following,
        primaryjoin=lambda: Artist.id == artist_following.c.artist_id,
        secondaryjoin=lambda: Artist.id == artist_following.c.following_id,
        backref='followers'
    )

    def __repr__(self):
        return f"{self.id} email={self.email}"

    def __init__(self, *args, **kwargs):
        """initializes artist"""
        super().__init__(*args, **kwargs)


artist_following = Table(
    'artist_following',
    Base.metadata,
    Column('artist_id', String(60), ForeignKey(Artist.id), primary_key=True),
    Column('following_id', String(60), ForeignKey(Artist.id), primary_key=True)
)
