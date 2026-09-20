from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Genre(Base):
    __tablename__ = "genres"

    genre_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    songs = relationship("Song", back_populates="genre")
