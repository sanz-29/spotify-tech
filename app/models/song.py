from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Song(Base):
    __tablename__ = "songs"

    song_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), nullable=False)
    artist_id = Column(Integer, ForeignKey("artists.artist_id"))
    album_id = Column(Integer, ForeignKey("albums.album_id"), nullable=True)
    genre_id = Column(Integer, ForeignKey("genres.genre_id"), nullable=True)
    audio_url = Column(String(255))
    cover_image_url = Column(String(255))
    duration = Column(Integer)

    artist = relationship("Artist", back_populates="songs")
    album = relationship("Album", back_populates="songs")
    genre = relationship("Genre", back_populates="songs")