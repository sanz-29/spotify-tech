from sqlalchemy import Column, Integer, String
from app.database import Base


class Song(Base):
    __tablename__ = "songs"

    song_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), nullable=False)
    artist_id = Column(Integer)
    album_id = Column(Integer, nullable=True)
    genre_id = Column(Integer, nullable=True)
    audio_url = Column(String(255))
    cover_image_url = Column(String(255))
    duration = Column(Integer)