from sqlalchemy import Column, Integer, String, Text
from app.database import Base


class Artist(Base):
    __tablename__ = "artists"

    artist_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    bio = Column(Text, nullable=True)
    image_url = Column(String(255), nullable=True)