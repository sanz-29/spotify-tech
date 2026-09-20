from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Playlist(Base):
    __tablename__ = "playlists"

    playlist_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    user = relationship("User", back_populates="playlists")
    playlist_songs = relationship(
        "PlaylistSong",
        back_populates="playlist",
        cascade="all, delete-orphan"
    )
    songs = relationship(
        "Song",
        secondary="playlist_songs",
        back_populates="playlists",
        viewonly=True
    )
