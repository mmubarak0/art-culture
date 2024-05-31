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
    Column("artist_id", String(60), ForeignKey("artists.id")),
    Column("artwork_id", String(60), ForeignKey("artworks.id")),
)


class Artwork(BaseModel, Base):
    """Artwork columns."""

    __tablename__ = "artworks"
    artist_id = Column(String(60), ForeignKey("artists.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(String(5000))
    views = Column(Integer, default=0)
    order = Column(Integer, default=0)
    media = relationship("Media", backref="artwork")
    comments = relationship("Comment", backref="artwork")
    likes = relationship("Artist", secondary=like_artwork, backref="liked_artworks")

    def to_dict(self):
        """Return dictionary representation of artwork"""
        likes_list = []
        for like in self.likes:
            likes_list.append(like.id)
        comments_list = []
        Comments = self.comments
        Comments.sort(key=lambda x: x.created_at)
        for comment in Comments:
            comments_list.append(comment.id)
        media_list = []
        Media = self.media
        for media in Media:
            media_list.append(media.id)
        return {
            **super().to_dict(),
            "likes": likes_list,
            "comments": comments_list,
            "media": media_list,
        }

    @property
    def get_media(self):
        result = []
        for media in self.media:
            result.append({"url": media.url, "type": media.type, "name": media.name})
        return result

    @property
    def number_of_likes(self):
        return f"{len(self.likes)}"

    @property
    def get_comments(self):
        result = []
        for comment in self.comments:
            result.append(
                {
                    "by": comment.artist.id,
                    "user_name": f"{comment.artist.first_name} "
                    f"{comment.artist.last_name}",
                    "content": comment.content,
                }
            )
        return result

    @property
    def liked_by(self):
        result = []
        for artist in self.likes:
            result.append(
                {
                    "by": artist.id,
                    "user_name": f"{artist.first_name} " f"{artist.last_name}",
                }
            )
        return result

    def __repr__(self):
        return f"({self.id}) title='{self.title}'"

    def __init__(self, *args, **kwargs):
        """initializes artwork"""
        super().__init__(*args, **kwargs)
