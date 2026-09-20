from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Album(Base):
    __tablename__ = "albums"

    album_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    artist_id = Column(Integer, ForeignKey("artists.artist_id"), nullable=True)
    release_date = Column(Date, nullable=True)
    cover_image_url = Column(String(255), nullable=True)

    artist = relationship("Artist", back_populates="albums")
    songs = relationship("Song", back_populates="album")
