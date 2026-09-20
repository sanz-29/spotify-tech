from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.database import Base


class PlaylistSong(Base):
    __tablename__ = "playlist_songs"

    playlist_id = Column(
        Integer,
        ForeignKey("playlists.playlist_id", ondelete="CASCADE"),
        primary_key=True
    )
    song_id = Column(
        Integer,
        ForeignKey("songs.song_id", ondelete="CASCADE"),
        primary_key=True
    )
    added_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    playlist = relationship("Playlist", back_populates="playlist_songs")
    song = relationship("Song", back_populates="playlist_songs")
